from typing import Optional
import grpc
import click
import toml

from quick_api_tests.generators.grpc.extractor import GrpcServiceExtractor
from quick_api_tests.generators.grpc.generator import GRPCGenerator
from quick_api_tests.generators.logic_generator.logic_generator import LogicGenerator
from quick_api_tests.generators.http.parser import OpenAPISpec
from quick_api_tests.generators.http.rest_codegen import HTTPGenerator
from quick_api_tests.generators.test_generator.generator import TestGenerator
from quick_api_tests.generators.utils import format_file


@click.group()
def cli() -> None: ...


@click.command("generate")
@click.option(
    "-t",
    "--type",
    "gentype",
    required=False,
    type=str,
    default=None,
    help="Concrete type of generation: grpc, http, etc.",
)
def generate_command(gentype: Optional[str] = None) -> None:
    with open("quick.toml") as config_file:
        config = toml.load(config_file)
        api_descriptors = []
        async_mode = config["base"][0]["async_mode"]
        if gentype == "grpc":
            for grpc_service in config["grpc"]:
                channel = grpc.insecure_channel(grpc_service["channel"])
                extractor = GrpcServiceExtractor(
                    channel=channel, service_name=grpc_service["service_name"]
                )
                api_descriptors.append(extractor)
                codegen = GRPCGenerator(
                    extractor=extractor,
                    async_mode=async_mode,
                )
                codegen.generate()
                logic = LogicGenerator(
                    server_address=grpc_service["channel"],
                    api_descriptor=extractor,
                    async_mode=async_mode,
                )
                logic.generate()
        elif gentype == "http":
            for http_service in config["http"]:
                openapi_spec = OpenAPISpec(
                    openapi_spec=http_service["swagger"],
                    service_name=http_service["service_name"],
                )
                api_descriptors.append(openapi_spec)
                codegen = HTTPGenerator(
                    openapi_spec=openapi_spec,
                    async_mode=async_mode,
                )
                codegen.generate()
                logic = LogicGenerator(
                    server_address=http_service["url"],
                    api_descriptor=openapi_spec,
                    async_mode=async_mode,
                )
                logic.generate()

        tests = TestGenerator(
            api_descriptors=api_descriptors,
            async_mode=async_mode,
        )
        tests.generate()
        format_file()


cli.add_command(generate_command)

if __name__ == "__main__":
    cli()
