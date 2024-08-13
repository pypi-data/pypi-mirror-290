from abc import (
    abstractmethod,
    ABC,
)
from typing import (
    Callable,
)

import grpc
from grpc.aio import (
    ClientInterceptor,
)
from grpc.aio._typing import ChannelArgumentType

from quick_api_tests.grpc_client.interceptors.logging import LoggerInterceptor

StubType = Callable[[grpc.Channel], object]


class BaseClient(ABC):
    async_mode = False

    def __init__(self, server_address: str) -> None:
        self.logging_interceptor = [LoggerInterceptor()]

        if self.async_mode:
            self.channel = grpc.aio.insecure_channel(
                target=server_address,
                # interceptors=self._interceptors,
                options=self.channel_options,
            )
        else:
            self.channel = grpc.insecure_channel(
                target=server_address,
                options=self.channel_options,
            )
            self.channel = grpc.intercept_channel(self.channel, *self._interceptors)

    @property
    def _interceptors(self) -> list | ClientInterceptor:
        return self.logging_interceptor + self.interceptors

    @property
    def interceptors(self) -> list | list[grpc.aio._interceptor.ClientInterceptor]:
        """
        Вы можете переопределить interceptors, если понимаете зачем вы это делаете.

        ```python
        class MyGrpcClient(BaseGrpcClient):
            interceptors = [InterceptorOne, InterceptorTwo]
            ...
        ```
        """
        return []

    @property
    def channel_options(self) -> list | ChannelArgumentType:
        """
        Вы можете переопределить channel_options, если понимаете зачем вы это делаете.

        Доступные опции здесь: https://grpc.github.io/grpc/core/group__grpc__arg__keys.html

        ```python
        class MyGrpcClient(BaseGrpcClient):
            channel_options = [
                ("grpc.max_receive_message_length", -1),
                ("grpc.max_send_message_length", -1),
            ]
        ```
        """
        return []

    @property
    @abstractmethod
    def stub_factory(self) -> StubType:
        pass

    def _do_call(self, stub_method: str, **kwargs) -> grpc.Call | grpc.aio.Call:  # type: ignore
        return getattr(self._get_stub(), stub_method)(**kwargs)

    def _get_stub(self) -> object:
        stub = self.stub_factory(self.channel)
        return stub
