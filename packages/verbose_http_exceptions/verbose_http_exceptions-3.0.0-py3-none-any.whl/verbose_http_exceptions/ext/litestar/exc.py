from verbose_http_exceptions import status
from verbose_http_exceptions.exc import (
    BaseHTTPExceptionWithNestedErrors,
    UnprocessableContentHTTPException,
)


class RequestValidationHTTPExceptionWithNestedErrors(BaseHTTPExceptionWithNestedErrors):
    """Litestar request validation http exception."""

    status_code = status.HTTP_400_BAD_REQUEST


class ValidationHTTPException(UnprocessableContentHTTPException):
    """Override for UnprocessableContentHTTPException but with code = 'validation_error'."""

    code = "validation_error"
