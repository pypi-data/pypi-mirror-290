from pathlib import Path
from subprocess import SubprocessError
from typing import Optional

from quick_api_tests.generators import TEMPLATES
from quick_api_tests.generators.base import BaseGenerator
from quick_api_tests.generators.http.parser import OpenAPISpec
from quick_api_tests.generators.utils import (
    create_and_write_file,
    run_command,
    is_url,
)
from quick_api_tests.generators.http.filters import (
    to_snake_case,
    to_camel_case,
)

from jinja2 import (
    Environment,
    FileSystemLoader,
)

from quick_api_tests.logger.log import LOGGER


class HTTPGenerator(BaseGenerator):
    BASE_PATH = Path('.') / "clients" / "http"

    def __init__(self, openapi_spec: OpenAPISpec, templates_dir: Optional[Path] = None, async_mode: bool = False) -> None:
        super().__init__()
        self.openapi_spec = openapi_spec
        self.templates_dir = templates_dir or TEMPLATES
        self.env = Environment(loader=FileSystemLoader(self.templates_dir), autoescape=True)
        self.env.filters["to_snake_case"] = to_snake_case
        self.env.filters["to_camel_case"] = to_camel_case
        self.async_mode = async_mode

    def generate(self) -> None:
        self._gen_clients()
        self._gen_init_apis()
        self._gen_models()

    def _gen_init_apis(self) -> None:

        rendered_code = self.env.get_template("http_apis_init.jinja2").render(
            api_names=self.openapi_spec.api_tags,
            service_name=self.openapi_spec.service_name,
        )
        file_name = f"{to_snake_case(self.openapi_spec.service_name)}/__init__.py"
        file_path = self.BASE_PATH / file_name
        create_and_write_file(file_path=file_path, text=rendered_code)
        create_and_write_file(file_path=file_path.parent.parent / "__init__.py", text="# coding: utf-8")

    def _gen_clients(self) -> None:
        for tag in self.openapi_spec.api_tags:
            LOGGER.info(f"Generate REST client for tag: {tag}")
            handlers = self.openapi_spec.handlers_by_api_name(tag)
            models = self.openapi_spec.models_by_api_name(tag)
            rendered_code = self.env.get_template("http_client.jinja2").render(
                async_mode=self.async_mode,
                models=models,
                data_list=handlers,
                api_name=tag,
                service_name=self.openapi_spec.service_name,
                version=self.openapi_spec.version,
            )
            file_name = f"{to_snake_case(tag)}_api.py"
            file_path = self.BASE_PATH / to_snake_case(self.openapi_spec.service_name) / "apis" / file_name
            create_and_write_file(file_path=file_path, text=rendered_code)
            create_and_write_file(file_path=file_path.parent / "__init__.py", text="# coding: utf-8")

    def _gen_models(self) -> None:
        LOGGER.info(f"Generate models for service: {self.openapi_spec.service_name}")
        file_path = self.BASE_PATH / to_snake_case(self.openapi_spec.service_name) / "models" / "api_models.py"
        spec = self.openapi_spec.cache_spec_path if is_url(self.openapi_spec.spec_path) else self.openapi_spec.spec_path
        create_and_write_file(file_path=file_path)
        create_and_write_file(file_path=file_path.parent / "__init__.py", text="# coding: utf-8")
        command = f"""datamodel-codegen \
                    --input {spec} \
                    --output {file_path} \
                    --snake-case-field \
                    --output-model-type pydantic_v2.BaseModel \
                    --reuse-model \
                    --capitalise-enum-members"""
        exit_code, stderr = run_command(command)
        if exit_code != 0:
            raise SubprocessError(stderr)
