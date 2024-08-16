from verbose_http_exceptions.exc.base import BaseVerboseHTTPException


class BaseHTTPExceptionWithNestedErrors(BaseVerboseHTTPException):
    """Verbose response with nested errors."""

    __skip_abstract_raise_error__ = True

    code = "multiple"
    type_ = "multiple"
    message = "Multiple errors ocurred. Please check list for nested_errors."
