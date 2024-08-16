"""Handlers for FastAPI."""

from typing import TYPE_CHECKING

from dev_utils.guards import all_dict_keys_are_str
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse, Response

from verbose_http_exceptions import error_by_status_mapping
from verbose_http_exceptions.ext.fastapi.exc import (
    RequestValidationHTTPExceptionWithNestedErrors,
    ValidationHTTPException,
)
from verbose_http_exceptions.ext.fastapi.utils import validation_error_from_error_dict

if TYPE_CHECKING:
    from fastapi import Request
    from fastapi.exceptions import RequestValidationError

    from verbose_http_exceptions.exc import BaseVerboseHTTPException


async def verbose_http_exception_handler(
    _: "Request",
    exc: "BaseVerboseHTTPException",
) -> "Response":
    """Handle verbose HTTP exception output.

    Handle only BaseVerboseHTTPException inherited instances. For handling all exceptions use
    ``any_http_exception_handler``.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.as_dict(),
        headers=exc.headers,
    )


async def verbose_request_validation_error_handler(
    _: "Request",
    exc: "RequestValidationError",
) -> "Response":
    """Handle RequestValidationError to override 422 error."""
    nested_errors: list[ValidationHTTPException] = []
    errors = exc.errors()
    if len(errors) == 1:
        error = errors[0]
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=validation_error_from_error_dict(error).as_dict(),
        )
    for error in errors:
        if not isinstance(error, dict):  # pragma: no cover
            continue
        if not all_dict_keys_are_str(error):  # type: ignore reportUnknownArgumentType # pragma: no cover
            continue
        nested_errors.append(validation_error_from_error_dict(error))
    main_error = RequestValidationHTTPExceptionWithNestedErrors(*nested_errors)
    return JSONResponse(
        status_code=main_error.status_code,
        content=main_error.as_dict(),
    )


async def any_http_exception_handler(
    _: "Request",
    exc: "HTTPException",
) -> "Response":
    """Handle any HTTPException errors (BaseVerboseHTTPException too).

    Doesn't handle 422 request error well. Use ``verbose_request_validation_error_handler`` for it.
    """
    class_ = error_by_status_mapping.get(exc.status_code)
    if class_ is None:
        response = JSONResponse(
            status_code=exc.status_code,
            content=exc.detail,
            headers=exc.headers,
        )
        if exc.status_code == status.HTTP_204_NO_CONTENT:  # pragma: no cover
            response.body = b''
        return response
    content = class_(message=exc.detail).as_dict()
    return JSONResponse(
        status_code=exc.status_code,
        content=content,
        headers=exc.headers,
    )
