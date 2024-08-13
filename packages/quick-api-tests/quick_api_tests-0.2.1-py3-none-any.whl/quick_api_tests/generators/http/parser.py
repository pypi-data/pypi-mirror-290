import re
from pathlib import Path

import httpx
import json
from typing import (
    Any,
    Optional,
    Union,
)
from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
)

from quick_api_tests.generators.base import BaseApiDescriptor
from quick_api_tests.generators.http.filters import (
    to_snake_case,
    to_camel_case,
)
from quick_api_tests.logger.log import LOGGER

TYPE_MAP = {
    "integer": "int",
    "number": "float",
    "string": "str",
    "boolean": "bool",
    "array": "list",
    "anyOf": "Any",
    None: "Any",
}

DEFAULT_HEADER_VALUE_MAP = {
    "int": 0,
    "float": 0.0,
    "str": "",
    "bool": True
}


class Handler(BaseModel):
    path: str = Field(...)
    method: str = Field(...)
    tags: list = Field(...)
    summary: Optional[str] = Field(None)
    operation_id: Optional[str] = Field(None)
    path_parameters: Optional[list] = Field(None)
    query_parameters: Optional[list] = Field(None)
    headers: Optional[list] = Field(None)
    request_body: Optional[str] = Field(None)
    responses: Optional[dict] = Field(None)

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


class OpenAPISpec(BaseApiDescriptor):
    BASE_PATH = Path.cwd() / "clients" / "http"

    def __init__(self, openapi_spec: Union[str, HttpUrl], service_name: str) -> None:
        self.spec_path = str(openapi_spec)
        self._service_name = service_name
        self.cache_spec_dir = self.BASE_PATH / to_snake_case(self.service_name)

        if not self.cache_spec_dir.exists():
            self.cache_spec_dir.mkdir(parents=True, exist_ok=True)

        self.cache_spec_path = str(self.cache_spec_dir / "swagger.json")

        self.openapi_spec: dict = self._open()
        self.version: str = ""
        self.description: str = ""
        self.openapi_version: str = ""
        self.api_tags: set[str] = set()
        self.handlers: list[Handler] = []
        self.request_models: set[str] = set()
        self.response_models: set[str] = set()
        self.parse_openapi_spec()

    @property
    def client_type(self) -> str:
        return "http"

    @property
    def apis(self) -> set[str]:
        return self.api_tags

    @staticmethod
    def _patch(swagger_scheme: dict) -> dict:
        """
        Patch swagger json file to avoid multi files gen.

        :param swagger_scheme: Swagger json
        """
        json_content = json.dumps(swagger_scheme)
        schemas = swagger_scheme.get("components", {}).get("schemas", {}) or swagger_scheme.get("definitions", {})
        schemas_to_patch = [schema for schema in schemas if "." in schema]

        for _, methods in swagger_scheme.get("paths", {}).items():
            for _, method in methods.items():
                for tag in method.get("tags", []):
                    if "." in tag:
                        schemas_to_patch.append(tag)

        for schema in schemas_to_patch:
            for text in [f'/{schema}"', f'"{schema}"']:
                json_content = json_content.replace(text, text.replace(".", ""))

        return json.loads(json_content)

    def _get_spec_by_url(self) -> Union[dict, None]:
        try:
            response = httpx.get(self.spec_path, timeout=5)
            response.raise_for_status()
        except httpx.HTTPStatusError:
            LOGGER.warning(f"OpenAPI spec not available by url: {self.spec_path} ")
            if Path(self.spec_path).is_file():
                LOGGER.warning(f"Try open OpenAPI spec by path: {self.spec_path}")
                with open(self.spec_path, "r") as f:
                    spec = self._patch(json.loads(f.read()))
            return spec
        else:
            spec = self._patch(response.json())
            with open(self.cache_spec_path, "w") as f:
                f.write(json.dumps(spec, indent=4, ensure_ascii=False))
            return spec

    def _get_spec_from_cache(self) -> dict:
        try:
            with open(self.cache_spec_path, "r") as f:
                spec = self._patch(json.loads(f.read()))
                self.spec_path = self.cache_spec_path
                LOGGER.warning(f"OpenAPI spec got from cash: {self.spec_path}")
                return spec
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"OpenAPI spec not available from url: {self.spec_path}, and not found in cash"
            ) from e

    def _get_spec_by_path(self) -> Union[dict, None]:
        try:
            with open(self.spec_path, "r") as f:
                spec = json.loads(f.read())
        except FileNotFoundError:
            LOGGER.warning(f"OpenAPI spec not found from local path: {self.spec_path}")
            return None
        else:
            return spec

    def _open(self) -> dict:
        spec = self._get_spec_by_url()
        if not spec:
            spec = self._get_spec_by_path()
        if not spec:
            spec = self._get_spec_from_cache()
        return spec

    def _get_request_body(self, request_body: Union[dict, list]) -> Union[str, None]:
        if isinstance(request_body, list):
            for parameter in request_body:
                if parameter.get("in") == "body":
                    schema = parameter.get("schema", {}).get("$ref", None)
                    if schema:
                        model_path = to_camel_case(schema.split("/")[-1])
                        model_name = model_path[0].upper() + model_path[1:]
                        self.request_models.add(model_name)
                        return model_name
        else:
            for content_type in request_body.get("content", {}).keys():
                schema = request_body.get("content", {}).get(content_type, {}).get("schema", {}).get("$ref", None)
                if schema:
                    model_name = to_camel_case(schema.split("/")[-1])
                    self.request_models.add(model_name)
                    return model_name
        return None

    def _get_response_body(self, response_body: dict) -> dict:
        responses: dict = {}
        if response_body:
            if self.openapi_version.startswith("3."):
                for status_code in response_body.keys():
                    for content_type in response_body.get(status_code, {}).get("content", {}).keys():
                        schema = (
                            response_body.get(status_code, {})
                            .get("content", {})
                            .get(content_type, {})
                            .get("schema", {})
                            .get("$ref", None)
                        )
                        model_name = schema.split("/")[-1] if schema else None
                        if model_name:
                            model_name = to_camel_case(model_name)
                            responses[status_code] = model_name
                            self.response_models.add(model_name)
            elif self.openapi_version.startswith("2."):
                for status_code, response in response_body.items():
                    ref_schema = response.get("schema", {}).get("$ref")
                    result_schema = response.get("schema", {}).get("result")
                    schema = ref_schema or result_schema
                    if schema:
                        model = to_camel_case(schema.split("/")[-1])
                        responses[status_code] = model
                        model_name = model[0].upper() + model[1:]
                        responses[status_code] = model_name
                        self.response_models.add(model_name)
        return responses

    def _get_headers(self, parameters: list) -> list:
        params = self._get_params_with_types(parameters, param_type="header")
        return params

    def _get_request_parameters(self, parameters: list) -> list:
        params = self._get_params_with_types(parameters, param_type="header")
        return params

    def _get_path_parameters(self, parameters: list) -> list:
        params = self._get_params_with_types(parameters, param_type="path")
        return params

    def _get_query_parameters(self, parameters: list) -> list:
        params = self._get_params_with_types(parameters, param_type="query")
        return params

    @staticmethod
    def _get_params_with_types(parameters: list, param_type: str) -> list:
        params: list[dict[str, str]] = []
        exclude_params = ["x-o3-app-name"]
        if not parameters:
            return params
        for parameter in parameters:
            if parameter.get("in") == param_type:
                parameter_type = parameter.get("schema", {})
                any_of = parameter_type.get("anyOf")
                enum = parameter_type.get("$ref")

                parameter_type = parameter_type.get("type")
                parameter_name = parameter.get("name")
                parameter_description = parameter.get("description", "")
                parameter_is_required = parameter.get("required", False)

                if parameter_name in exclude_params:
                    continue

                if any_of:
                    parameter_type = "anyOf"
                if enum:
                    parameter_type = enum.split("/")[-1]

                parameter_with_desc = {
                    "name": parameter_name,
                    "type": parameter_type if enum else TYPE_MAP[parameter_type],
                    "description": parameter_description,
                    "required": parameter_is_required,
                }

                if not parameter_is_required:
                    parameter_with_desc["default"] = DEFAULT_HEADER_VALUE_MAP.get(TYPE_MAP.get(parameter_type, ""))
                params.append(parameter_with_desc)

        return params

    @staticmethod
    def _normalize_swagger_path(path: str) -> str:
        def replace_placeholder(match: re.Match) -> str:
            placeholder = match.group(0)[1:-1]
            return "{" + to_snake_case(placeholder) + "}" if placeholder else ""

        normalized_path = re.sub(r"\{[^}]*\}", replace_placeholder, path)
        return normalized_path

    def parse_openapi_spec(self) -> list[Handler]:
        info = self.openapi_spec.get("info", {})
        self.version = info.get("version", "1.0.0")
        self.description = info.get("description", "")
        self.openapi_version = self.openapi_spec.get("openapi", "") or self.openapi_spec.get("swagger", "")

        paths = self.openapi_spec.get("paths", {})
        for path, methods in paths.items():
            for method, details in methods.items():
                self._process_method(path, method, details)
        return self.handlers

    def _process_method(self, path: str, method: str, details: dict) -> None:
        tags = details.get("tags", [])
        for tag in tags:
            self.api_tags.add(tag)

        summary = details.get("summary", "")
        operation_id = details.get("operationId", "")
        parameters = details.get("parameters", [])
        query_parameters = self._get_query_parameters(parameters)
        path_parameters = self._get_path_parameters(parameters)
        headers = self._get_headers(parameters)
        request_body = self._get_request_body(details.get("requestBody", details.get("parameters", {})))
        responses = self._get_response_body(details.get("responses", {}))

        path_obj = Handler(
            path=self._normalize_swagger_path(path),
            method=method,
            tags=tags,
            summary=summary,
            operation_id=operation_id,
            query_parameters=query_parameters,
            headers=headers,
            path_parameters=path_parameters,
            request_body=request_body,
            responses=responses,
        )
        self.handlers.append(path_obj)

    def models_by_api_name(self, api_name: str) -> set[str]:
        models = set()
        for handler in self.handlers:
            if api_name in handler.tags:
                if handler.path_parameters is not None:
                    for param in handler.path_parameters:
                        param = param["type"]
                        if param not in TYPE_MAP.values():
                            models.add(param)
                if handler.query_parameters is not None:
                    for query_param in handler.query_parameters:
                        query_param = query_param["type"]
                        if query_param not in TYPE_MAP.values():
                            models.add(query_param)
                if handler.headers is not None:
                    for header_param in handler.headers:
                        header_param = header_param["type"]
                        if header_param not in TYPE_MAP.values():
                            models.add(header_param)
                if handler.request_body is not None:
                    models.add(handler.request_body)
                if handler.responses is not None:
                    models.update(handler.responses.values())
        return models

    def handlers_by_api_name(self, api_name: str) -> list[Handler]:
        return [h for h in self.handlers if api_name in h.tags]

    def handlers_by_method_type(self, method_type: str) -> list[Handler]:
        return [h for h in self.handlers if h.method == method_type]

    def handler_by_path(self, path: str) -> list[Handler]:
        return [h for h in self.handlers if h.path == path]

    @property
    def service_name(self) -> str:
        return self._service_name
