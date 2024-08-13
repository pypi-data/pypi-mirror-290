from typing import (
    Iterable,
)

import grpc
import structlog
from grpc_status import rpc_status
from google.protobuf.message import Message
from collections import UserDict
from google.protobuf.json_format import MessageToDict


def log_request(
        log: structlog.BoundLogger,
        call_details: grpc.ClientCallDetails,
        request: Message
):
    log.msg(
        "request",
        method=call_details.method,
        request_data=MessageToDict(request),
        metadata=UserDict(call_details.metadata),
    )


def log_request_iterator(
        log: structlog.BoundLogger,
        call_details: grpc.ClientCallDetails,
        request_iterator: Iterable[Message],
):
    try:
        for request in request_iterator:
            log.msg(
                "request",
                method=call_details.method,
                request_data=MessageToDict(request),
                metadata=UserDict(call_details.metadata),
            )
            yield request
    except Exception as e:
        log.msg(
            "error",
            message="An error occurred while iterating over requests",
            error=str(e),
        )
        raise


def log_response_iterator(log: structlog.BoundLogger, response_iterator):
    metadata = {}
    try:
        log.msg("debug", message="Starting to iterate over responses")
        for response in response_iterator:
            log.msg(
                "response",
                response=MessageToDict(
                    response,
                    always_print_fields_with_no_presence=True,
                ),
            )
            yield response
    except Exception as e:
        metadata = {
            **trailing_metadata(response_iterator),
            **initial_metadata(response_iterator),
        }
        log.msg(
            "error",
            status_сode=response_iterator.code().name,
            details=response_iterator.exception().details(),
            metadata=metadata,
        )
        raise
    finally:
        log.msg("response", metadata=metadata)
        log.msg("debug", message="Finished iterating over responses")


def log_response(log, response):
    metadata = {**trailing_metadata(response), **initial_metadata(response)}
    if not _response_has_error(response):
        log.msg(
            "response",
            response=MessageToDict(
                response.result(),
                always_print_fields_with_no_presence=True,
            ),
            metadata=metadata,
        )
    else:
        log.msg(
            "error",
            statusCode=response.code().name,
            details=response.exception().details(),
            metadata=metadata,
        )


def trailing_metadata(response: grpc.Call) -> UserDict:
    """
    Get trailing metadata of response
    """
    trailing_metadata_dict = UserDict(response.trailing_metadata())
    if rpc_status.GRPC_DETAILS_METADATA_KEY in trailing_metadata_dict:
        del trailing_metadata_dict[rpc_status.GRPC_DETAILS_METADATA_KEY]
    return trailing_metadata_dict


def initial_metadata(response: grpc.Call) -> UserDict:
    """
    Get initial metadata of response
    """
    return UserDict(response.initial_metadata())


def _response_has_error(response: grpc.RpcError) -> bool:
    """
    Check that response contains errors

    :param response:
    :return: True or False
    """
    exc = response.exception()
    return isinstance(exc, grpc.RpcError)
