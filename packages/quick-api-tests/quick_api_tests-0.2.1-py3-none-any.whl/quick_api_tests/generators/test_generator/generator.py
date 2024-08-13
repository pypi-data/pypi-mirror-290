from pathlib import Path
from typing import Optional

from jinja2 import Environment, FileSystemLoader

from quick_api_tests.generators import TEMPLATES
from quick_api_tests.generators.base import BaseGenerator, BaseApiDescriptor
from quick_api_tests.generators.http.filters import to_snake_case, to_camel_case
from quick_api_tests.generators.utils import create_and_write_file
from quick_api_tests.logger.log import LOGGER
from collections import namedtuple

Service = namedtuple("Service", ["name", "client_type"])


class TestGenerator(BaseGenerator):
    BASE_PATH = Path(".") / "tests"

    def __init__(
        self,
        api_descriptors: list[BaseApiDescriptor],
        templates_dir: Optional[Path] = None,
        async_mode: bool = False,
    ):
        super().__init__()
        self.api_descriptors = api_descriptors
        self.templates_dir = templates_dir or TEMPLATES
        self.env = Environment(
            loader=FileSystemLoader(self.templates_dir), autoescape=True
        )
        self.env.filters["to_snake_case"] = to_snake_case
        self.env.filters["to_camel_case"] = to_camel_case
        self.async_mode = async_mode

    def generate(self) -> None:
        self._gen_tests()
        self._gen_base_setup()

    def _gen_tests(self):
        for api_descriptor in self.api_descriptors:
            for api in api_descriptor.apis:
                LOGGER.info(f"Generate client logic for: {api}")

                async_mode = self.async_mode
                handlers = api_descriptor.handlers_by_api_name(api)
                service_name = api_descriptor.service_name
                client_type = api_descriptor.client_type
                for handler in handlers:
                    rendered_code = self.env.get_template("tests.jinja2").render(
                        handler,
                        api_name=api,
                        service_name=service_name,
                        async_mode=async_mode,
                        client_type=client_type,
                    )
                    file_name = (
                        f"test_{to_snake_case(handler.method + handler.path)}.py"
                    )
                    file_path = (
                        self.BASE_PATH
                        / client_type
                        / to_snake_case(service_name)
                        / to_snake_case(api)
                        / file_name
                    )
                    if file_path.exists():
                        LOGGER.info(f"File: {file_path} exists, skip generate!")
                    else:
                        create_and_write_file(file_path=file_path, text=rendered_code)

    def _gen_base_setup(self) -> None:
        LOGGER.info("Generate base setup")
        rendered_code = self.env.get_template("base_setup.jinja2").render(
            api_descriptors=self.api_descriptors,
            async_mode=self.async_mode,
        )
        file_path = self.BASE_PATH / "base_setup.py"
        create_and_write_file(file_path=file_path, text=rendered_code)
