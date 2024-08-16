from typing import TYPE_CHECKING, Any

from dev_utils.guards import all_dict_keys_are_str
from litestar import MediaType, Request, Response

from verbose_http_exceptions import error_by_status_mapping, status
from verbose_http_exceptions.exc.server_error import InternalServerErrorHTTPException
from verbose_http_exceptions.ext.litestar.constants import NO_CONTENT_STATUS_CODES
from verbose_http_exceptions.ext.litestar.exc import (
    RequestValidationHTTPExceptionWithNestedErrors,
    ValidationHTTPException,
)
from verbose_http_exceptions.ext.litestar.utils import validation_error_from_error_dict

if TYPE_CHECKING:
    from litestar.exceptions import HTTPException, ValidationException

    from verbose_http_exceptions.exc.base import BaseVerboseHTTPException, VerboseHTTPExceptionDict


def verbose_http_exception_handler(
    _: "Request[Any, Any, Any]",
    exc: "BaseVerboseHTTPException",
) -> "Response[VerboseHTTPExceptionDict]":
    """Handle verbose HTTP exception output.

    Handle only BaseVerboseHTTPException inherited instances. For handling all exceptions use
    ``any_http_exception_handler``.
    """
    return Response["VerboseHTTPExceptionDict"](
        media_type=MediaType.JSON,
        status_code=exc.status_code,
        content=exc.as_dict(),
        headers=exc.headers,
    )


def verbose_request_validation_error_handler(
    _: "Request[Any, Any, Any]",
    exc: "ValidationException",
) -> "Response[VerboseHTTPExceptionDict]":
    """Handle ValidationException to override 400 error."""
    nested_errors: list[ValidationHTTPException] = []
    errors = exc.extra
    if errors is None or (isinstance(errors, list) and len(errors) == 0):
        errors = [{"message": exc.detail, "source": None, "key": None, "type": None}]
    # NOTE: not sure, is it possible to handle such condition.
    if isinstance(errors, dict):  # pragma: no cover
        errors = [errors]
    if len(errors) == 1:
        error = errors[0]
        return Response["VerboseHTTPExceptionDict"](
            media_type=MediaType.JSON,
            status_code=status.HTTP_400_BAD_REQUEST,
            content=validation_error_from_error_dict(error).as_dict(),
            headers=exc.headers,
        )
    for error in errors:
        if not isinstance(error, dict):  # pragma: no cover
            continue
        if not all_dict_keys_are_str(error):  # type: ignore[reportUnknownArgumentType] # pragma: no cover
            continue
        nested_errors.append(validation_error_from_error_dict(error))
    main_error = RequestValidationHTTPExceptionWithNestedErrors(*nested_errors)
    return Response["VerboseHTTPExceptionDict"](
        media_type=MediaType.JSON,
        status_code=main_error.status_code,
        content=main_error.as_dict(),
        headers=exc.headers,
    )


def any_http_exception_handler(
    _: "Request[Any, Any, Any]",
    exc: "HTTPException",
) -> "Response[VerboseHTTPExceptionDict | str | None]":
    """Handle any HTTPException errors (BaseVerboseHTTPException too).

    Doesn't handle 422 request error well. Use ``verbose_request_validation_error_handler`` for it.
    """
    class_ = error_by_status_mapping.get(exc.status_code)
    is_no_content = exc.status_code in NO_CONTENT_STATUS_CODES
    if class_ is None or is_no_content:
        content = None if is_no_content else exc.detail
        media_type = MediaType.TEXT if is_no_content else MediaType.JSON
        return Response(
            media_type=media_type,
            status_code=exc.status_code,
            content=content,
            headers=exc.headers,
        )
    content = class_(message=exc.detail).as_dict()
    return Response(
        media_type=MediaType.JSON,
        status_code=exc.status_code,
        content=content,
        headers=exc.headers,
    )


def python_error_handler(
    _: "Request[Any, Any, Any]",
    exc: "Exception",
) -> "Response[VerboseHTTPExceptionDict]":
    """Handle any Python exception like Exception or ValueError."""
    return Response["VerboseHTTPExceptionDict"](
        media_type=MediaType.JSON,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=InternalServerErrorHTTPException(message=str(exc)).as_dict(),
    )
