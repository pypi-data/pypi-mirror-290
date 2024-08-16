"""FastAPI extension for verbose http exceptions usage."""

from verbose_http_exceptions.ext.pydantic_schemas import (
    VerboseHTTPExceptionSchema as VerboseHTTPExceptionSchema,
)

# NOTE: too long names to fit them in 100 chars (line max length).
from .appliers import apply_all_handlers as apply_all_handlers
from .appliers import apply_any_http_exception_handler as apply_any_http_exception_handler
from .appliers import (
    apply_python_errors_handling_middleware as apply_python_errors_handling_middleware,
)
from .appliers import apply_verbose_http_exception_handler as apply_verbose_http_exception_handler
from .appliers import (
    apply_verbose_request_validation_error_handler,  # type: ignore[reportUnusedImport]
)
from .exc import RequestValidationHTTPExceptionWithNestedErrors  # type: ignore[reportUnusedImport]
from .exc import ValidationHTTPException as ValidationHTTPException
from .handlers import any_http_exception_handler as any_http_exception_handler
from .handlers import verbose_http_exception_handler as verbose_http_exception_handler
from .handlers import (
    verbose_request_validation_error_handler as verbose_request_validation_error_handler,
)
from .middlewares import python_errors_handling_middleware as python_errors_handling_middleware
from .openapi_override import override_422_error as override_422_error
from .utils import resolve_error_location_and_attr as resolve_error_location_and_attr
from .utils import validation_error_from_error_dict as validation_error_from_error_dict
