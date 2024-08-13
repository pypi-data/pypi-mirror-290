import re
from pathlib import Path
from typing import Optional

from quick_api_tests.generators import TEMPLATES
from quick_api_tests.generators.base import (
    BaseGenerator,
    BaseApiDescriptor,
)
from quick_api_tests.logger.log import LOGGER
from quick_api_tests.generators.utils import (
    create_and_write_file,
)
from quick_api_tests.generators.http.filters import (
    to_snake_case,
    to_camel_case,
)

from jinja2 import (
    Environment,
    FileSystemLoader,
)


class LogicGenerator(BaseGenerator):
    BASE_PATH = Path(".") / "logic"

    def __init__(
        self,
        api_descriptor: BaseApiDescriptor,
        server_address: Optional[str] = None,
        templates_dir: Optional[Path] = None,
        async_mode: bool = False,
    ):
        super().__init__()
        self.api_descriptor = api_descriptor
        self.server_address = server_address
        self.templates_dir = templates_dir or TEMPLATES
        self.env = Environment(
            loader=FileSystemLoader(self.templates_dir), autoescape=True
        )
        self.env.filters["to_snake_case"] = to_snake_case
        self.env.filters["to_camel_case"] = to_camel_case
        self.client_type = self.api_descriptor.client_type
        self.BASE_PATH = self.BASE_PATH / self.client_type
        self.async_mode = async_mode

    def generate(self):
        self._gen_client_wrappers()
        self._gen_facade()
        self._gen_logic_facade()

    def _gen_client_wrappers(self):
        for tag in self.api_descriptor.apis:
            LOGGER.info(f"Generate client logic for: {tag}")

            async_mode = self.async_mode
            client_type = self.api_descriptor.client_type
            models = self.api_descriptor.models_by_api_name(tag)
            handlers = self.api_descriptor.handlers_by_api_name(tag)
            service_name = self.api_descriptor.service_name
            rendered_code = self.env.get_template("client_logic.jinja2").render(
                async_mode=async_mode,
                client_type=client_type,
                models=models,
                handlers=handlers,
                api_name=tag,
                service_name=service_name,
            )
            file_name = f"{to_snake_case(self.api_descriptor.service_name)}/{to_snake_case(tag)}_api.py"
            file_path = self.BASE_PATH / file_name
            if file_path.exists():
                self._append_http_method(async_mode, file_path, handlers)
            else:
                create_and_write_file(file_path=file_path, text=rendered_code)

    def _append_http_method(self, async_mode, file_path, handlers):
        LOGGER.info(f"File: {file_path} exists!")
        with open(file_path, "r+") as file:
            text = file.read()
            for handler in handlers:
                search = to_snake_case(handler.method + handler.path)
                if not re.search(rf"{search}\(", text, re.MULTILINE):
                    method_code = self.env.get_template(
                        "http_logic_method.jinja2"
                    ).render(
                        handler,
                        async_mode=async_mode,
                    )
                    file.write(method_code)
                    LOGGER.info(
                        f"File: {file_path} is up to date with new method {handler.method + handler.path}!"
                    )

    def _gen_facade(self):
        LOGGER.info(
            f"Generate wrapper facade for service: {self.api_descriptor.service_name}"
        )
        rendered_code = self.env.get_template("wrapper_facade.jinja2").render(
            client_type=self.api_descriptor.client_type,
            api_names=self.api_descriptor.apis,
            service_name=self.api_descriptor.service_name,
        )
        file_name = f"{to_snake_case(self.api_descriptor.service_name)}/__init__.py"
        file_path = self.BASE_PATH / file_name
        create_and_write_file(file_path=file_path, text=rendered_code)

    def _gen_logic_facade(self):
        LOGGER.info(
            f"Generate logic facade for service: {self.api_descriptor.service_name}"
        )
        rendered_code = self.env.get_template("logic_facade.jinja2").render(
            server_address=self.server_address,
            client_type=self.api_descriptor.client_type,
            api_names=self.api_descriptor.apis,
            service_name=self.api_descriptor.service_name,
        )
        service_name = to_snake_case(self.api_descriptor.service_name)
        file_name = f"{service_name}_facade.py"
        file_path = self.BASE_PATH / service_name / file_name
        if file_path.exists():
            LOGGER.warning(f"File: {file_path} exists, skip generate!")
            return
        create_and_write_file(file_path=file_path, text=rendered_code)
