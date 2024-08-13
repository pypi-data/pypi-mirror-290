"""Module with interceptors for setting default headers for all handlers"""

import grpc

from collections import UserDict


class HeaderInterceptor(grpc.UnaryUnaryClientInterceptor):
    def __init__(self, headers: dict):
        """
        Create interceptor for setting default headers

        :param headers: default headers
        """
        self._headers = headers if headers else {}

    def intercept_unary_unary(self, continuation, call_details, request):
        """
        Set headers before sending every unary-unary requests
        """
        metadata = self._headers.copy()
        metadata.update(UserDict(call_details.metadata))
        return continuation(
            call_details._replace(
                metadata=[
                    *{
                        **metadata
                    }.items()
                ]
            ),
            request
        )
