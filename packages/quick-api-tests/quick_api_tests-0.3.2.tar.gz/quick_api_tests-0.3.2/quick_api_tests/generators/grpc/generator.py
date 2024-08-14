import pprint
from pathlib import Path
import grpc
from jinja2 import (
    Environment,
    FileSystemLoader,
)

from quick_api_tests.generators import TEMPLATES
from quick_api_tests.generators.base import BaseGenerator
from quick_api_tests.generators.grpc.extractor import GrpcServiceExtractor
from quick_api_tests.generators.grpc.proto_recover import ProtoRecover
from quick_api_tests.generators.http.filters import (
    to_snake_case,
    to_camel_case,
)
from quick_api_tests.generators.utils import (
    run_command,
    create_and_write_file,
)
from quick_api_tests.logger.log import LOGGER


class GRPCGenerator(BaseGenerator):
    BASE_PATH = Path(".") / "clients" / "grpc" / "internal"

    def __init__(self, extractor: GrpcServiceExtractor, async_mode: bool = False) -> None:
        super().__init__()
        self._extractor = extractor
        self._service_name = extractor.service_name
        self.templates_dir = TEMPLATES
        self.env = Environment(
            loader=FileSystemLoader(self.templates_dir), autoescape=True
        )
        self.env.filters["to_snake_case"] = to_snake_case
        self.env.filters["to_camel_case"] = to_camel_case
        self.proto_files = {}
        self.async_mode = async_mode

    def generate(self):
        self._recover_protos()
        self._generate_base_stubs()
        self._gen_clients()

    def _gen_clients(self):
        for stub in self._extractor.stub_names:
            LOGGER.info(f"Generate client for: {stub}")
            handlers = self._extractor.handlers_by_api_name(stub)
            imports = self._get_imports_path(stub)
            rendered_code = self.env.get_template("grpc_client.jinja2").render(
                async_mode=self.async_mode,
                imports=imports,
                handlers=handlers,
                stub_name=stub,
            )
            file_name = f"{to_snake_case(stub)}_pb.py"
            file_path = self.BASE_PATH.parent / "stubs" / to_snake_case(self._service_name) / file_name
            create_and_write_file(file_path=file_path, text=rendered_code)
            create_and_write_file(
                file_path=file_path.parent / "__init__.py", text="# coding: utf-8"
            )
            create_and_write_file(
                file_path=file_path.parent.parent / "__init__.py", text="# coding: utf-8"
            )

    def _get_imports_path(self, stub: str) -> list[str]:
        for proto_key, proto in self.proto_files.items():
            if stub == proto_key:
                proto = str(proto)
                stub_bp_grpc = proto.replace(".proto", '_pb2_grpc').replace("/", ".").replace("-", "_")
                models_pb = proto.replace(".proto", '_pb2').replace("/", ".").replace("-", "_")
                stub_import = f'from {stub_bp_grpc} import {stub}Stub'
                models_import = f'from {models_pb} import *'
                return [stub_import, models_import]

        return []

    def _generate_base_stubs(self):
        proto_files = self.BASE_PATH.rglob("*.proto")
        base_command = [
            "python",
            "-m",
            "grpc.tools.protoc",
            "-I .",
            "--proto_path=./clients/grpc/internal",
            "--python_out=.",
            "--grpc_python_out=.",
            "--mypy_out=.",
        ]
        for proto_file in proto_files:
            LOGGER.info(f"Generate stubs for proto: {proto_file}")
            command = " ".join(base_command + [str(proto_file)])
            exit_code, stderr = run_command(command)
            if exit_code != 0:
                LOGGER.error(f"Error generating stubs for {proto_file}: {stderr}")
                continue

    def _recover_protos(self):
        for proto_descriptor in self._extractor.proto_file_descriptors.values():
            proto_key = proto_descriptor.name
            if proto_descriptor.service:
                proto_key = proto_descriptor.service[0].name

            LOGGER.info(f"Processing recover proto: {proto_descriptor.name}")
            try:
                self.proto_files[proto_key] = ProtoRecover(proto_descriptor).get_proto(output_dir=self.BASE_PATH)
            except TypeError as e:
                LOGGER.error(f"Error processing: {proto_descriptor.name}: {e}")
