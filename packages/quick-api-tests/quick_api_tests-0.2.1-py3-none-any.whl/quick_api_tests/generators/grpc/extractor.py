import re
from typing import (
    Iterable,
    Any,
)

import grpc
from grpc_reflection.v1alpha import (
    reflection_pb2,
    reflection_pb2_grpc,
)
from google.protobuf import descriptor_pb2
from pydantic import BaseModel

from quick_api_tests.generators.base import BaseApiDescriptor


class Handler(BaseModel):
    stub_name: str
    stub_method: str
    request: str
    response: str
    method_type: str

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


class GrpcServiceExtractor(BaseApiDescriptor):

    def __init__(self, channel: grpc.Channel, service_name: str) -> None:
        self._channel = channel
        self._service_name = service_name
        self._reflection_stub = reflection_pb2_grpc.ServerReflectionStub(self._channel)
        self.stub_names: set[str] = set()
        self.proto_file_descriptors: dict[str, descriptor_pb2.FileDescriptorProto] = {}
        self.handlers: list[Handler] = []
        self._extract()

    @property
    def apis(self) -> set[str]:
        return self.stub_names

    @property
    def service_name(self) -> str:
        return self._service_name

    @property
    def client_type(self) -> str:
        return "grpc"

    def _extract(self) -> None:
        services = self._get_stub_names()
        self._fetch_proto_files(services)

    def _get_stub_names(self) -> list[str]:
        services_response = self._reflection_stub.ServerReflectionInfo(
            iter([reflection_pb2.ServerReflectionRequest(list_services="")])
        )
        full_stub_names = [
            service.name
            for service in next(services_response).list_services_response.service
        ]
        self.stub_names = {_.split(".")[-1] for _ in full_stub_names}
        return full_stub_names

    def _fetch_proto_files(self, full_stub_names: list[str]) -> None:
        for service_name in full_stub_names:
            file_protos = self._get_file_protos(service_name)
            for file_proto_response in file_protos:
                self._process_proto_response(file_proto_response)

    def _get_file_protos(
        self, stub_name: str
    ) -> Iterable[reflection_pb2.ServerReflectionResponse]:
        file_symbol_requests = [
            reflection_pb2.ServerReflectionRequest(file_containing_symbol=stub_name)
        ]
        return self._reflection_stub.ServerReflectionInfo(iter(file_symbol_requests))

    def _process_proto_response(
        self, file_proto_response: reflection_pb2.ServerReflectionResponse
    ) -> None:
        for (
            proto_bytes
        ) in file_proto_response.file_descriptor_response.file_descriptor_proto:
            file_descriptor_proto = descriptor_pb2.FileDescriptorProto()
            file_descriptor_proto.ParseFromString(proto_bytes)
            self.proto_file_descriptors[file_descriptor_proto.name] = file_descriptor_proto
            self._get_handlers(file_descriptor_proto)

    def _get_handlers(
        self, file_descriptor_proto: descriptor_pb2.FileDescriptorProto
    ) -> None:
        for service in file_descriptor_proto.service:
            for method in service.method:
                if method.client_streaming and method.server_streaming:
                    method_type = "StreamStream"
                elif method.client_streaming:
                    method_type = "StreamUnary"
                elif method.server_streaming:
                    method_type = "UnaryStream"
                else:
                    method_type = "UnaryUnary"

                handler = Handler(
                    stub_name=service.name,
                    stub_method=method.name,
                    request=method.input_type.split(".")[-1],
                    response=method.output_type.split(".")[-1],
                    method_type=method_type,
                )
                if handler not in self.handlers:
                    self.handlers.append(handler)

    def models_by_api_name(self, api_name: str) -> None:
        models = set()
        for handler in self.handlers:
            if handler.stub_name == api_name:
                models.add(handler.request)
                models.add(handler.response)

    def handlers_by_api_name(self, api_name: str) -> list[Handler]:
        return [h for h in self.handlers if h.stub_name == api_name]

    def handlers_by_method_type(self, method_type: str) -> list[Handler]:
        return [h for h in self.handlers if h.method_type == method_type]

    def handler_by_stub_method(self, stub_method: str) -> Handler:
        return [h for h in self.handlers if h.stub_method == stub_method][0]
