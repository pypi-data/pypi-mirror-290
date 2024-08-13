import uuid
from typing import (
    Callable,
    Iterable,
)

import grpc
import structlog
from google.protobuf.message import Message

from quick_api_tests.grpc_client.interceptors.log_utils import (
    log_response,
    log_request_iterator,
    log_response_iterator,
    log_request,
)


class LoggerInterceptor(
    grpc.UnaryUnaryClientInterceptor,
    grpc.UnaryStreamClientInterceptor,
    grpc.StreamUnaryClientInterceptor,
    grpc.StreamStreamClientInterceptor,
):
    def __init__(self):
        self.log = structlog.get_logger(self.__class__.__name__).bind(service="grpc")

    def intercept_unary_unary(
            self,
            continuation: Callable,
            call_details: grpc.ClientCallDetails,
            request: Message,
    ):
        """
        Logging for every unary-unary requests
        """
        log = self.log.bind(request_id=str(uuid.uuid4()))
        log_request(log=log, call_details=call_details, request=request)
        response = continuation(call_details, request)
        log_response(log, response)
        return response

    def intercept_unary_stream(
            self,
            continuation: Callable,
            call_details: grpc.ClientCallDetails,
            request: Message,
    ):
        """
        Logging for every unary-stream requests
        """
        log = self.log.bind(request_id=str(uuid.uuid4()))
        log_request(log=log, call_details=call_details, request=request)
        response_iterator = continuation(call_details, request)

        return log_response_iterator(log=log, response_iterator=response_iterator)

    def intercept_stream_stream(
            self,
            continuation: Callable,
            call_details: grpc.ClientCallDetails,
            request_iterator: Iterable[Message],
    ):
        """
        Logging for every stream-stream (bi-directional) requests and responses.
        """
        log = self.log.bind(request_id=str(uuid.uuid4()))

        logged_request_iterator = log_request_iterator(
            log=log, call_details=call_details, request_iterator=request_iterator
        )
        response_iterator = continuation(call_details, logged_request_iterator)

        return log_response_iterator(log=log, response_iterator=response_iterator)

    def intercept_stream_unary(
            self,
            continuation: Callable,
            call_details: grpc.ClientCallDetails,
            request_iterator: Iterable[Message],
    ):
        """
        Logging for every stream-unary (uni-directional) requests and response.
        """
        log = self.log.bind(request_id=str(uuid.uuid4()))

        logged_request_iterator = log_request_iterator(
            log=log, call_details=call_details, request_iterator=request_iterator
        )

        response = continuation(call_details, logged_request_iterator)
        log_response(log, response)
        return response
