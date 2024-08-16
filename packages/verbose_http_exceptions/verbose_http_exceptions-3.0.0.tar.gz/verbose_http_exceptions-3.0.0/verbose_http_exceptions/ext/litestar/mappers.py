from litestar.exceptions import HTTPException, ValidationException

from verbose_http_exceptions.exc.base import BaseVerboseHTTPException
from verbose_http_exceptions.ext.litestar import (
    any_http_exception_handler,
    python_error_handler,
    verbose_http_exception_handler,
    verbose_request_validation_error_handler,
)
from verbose_http_exceptions.ext.litestar.types import LitestarExceptionHandlersMap

VERBOSE_EXCEPTION_HANDLER_MAP: LitestarExceptionHandlersMap = {
    BaseVerboseHTTPException: verbose_http_exception_handler,  # type: ignore[reportAssignmentType]
}
LITESTAR_HTTP_EXCEPTION_HANDLER_MAP: LitestarExceptionHandlersMap = {
    HTTPException: any_http_exception_handler,  # type: ignore[reportAssignmentType]
}
LITESTAR_VALIDATION_EXCEPTION_HANDLER_MAP: LitestarExceptionHandlersMap = {
    ValidationException: verbose_request_validation_error_handler,  # type: ignore[reportAssignmentType]
}
PYTHON_EXCEPTION_HANDLER_MAP: LitestarExceptionHandlersMap = {
    Exception: python_error_handler,
}
ALL_EXCEPTION_HANDLERS_MAP: LitestarExceptionHandlersMap = {
    **VERBOSE_EXCEPTION_HANDLER_MAP,
    **LITESTAR_HTTP_EXCEPTION_HANDLER_MAP,
    **LITESTAR_VALIDATION_EXCEPTION_HANDLER_MAP,
    **PYTHON_EXCEPTION_HANDLER_MAP,
}
