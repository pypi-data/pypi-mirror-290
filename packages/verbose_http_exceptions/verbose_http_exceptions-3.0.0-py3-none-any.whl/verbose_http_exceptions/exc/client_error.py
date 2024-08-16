from string import Template

from verbose_http_exceptions import status
from verbose_http_exceptions.exc.base import BaseVerboseHTTPException


class BaseClientHTTPException(BaseVerboseHTTPException):
    """Base client error HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#client_error_responses for more
    information.
    """

    __skip_abstract_raise_error__ = True

    code = "client_error"


class BadRequestHTTPException(BaseClientHTTPException):
    """Bad request 400 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400 for more information.
    """

    status_code = status.HTTP_400_BAD_REQUEST
    type_ = "bad_request"
    message = "Incorrect request data."
    template = Template("Incorrect request data: $reason.")


class UnauthorizedHTTPException(BaseClientHTTPException):
    """Bad request 401 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/401 for more information.
    """

    status_code = status.HTTP_401_UNAUTHORIZED
    type_ = "unauthorized"
    message = "Unauthorized user."
    template = Template("Unauthorized user: $reason.")


class PaymentRequiredHTTPException(BaseClientHTTPException):
    """Payment required 402 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/402 for more information.
    """

    status_code = status.HTTP_402_PAYMENT_REQUIRED
    type_ = "payment_required"
    message = "Payment required."
    template = Template("Payment required: $reason.")


class ForbiddenHTTPException(BaseClientHTTPException):
    """Forbidden 403 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/403 for more information.
    """

    status_code = status.HTTP_403_FORBIDDEN
    type_ = "forbidden"
    message = "Permission denied."
    template = Template("Permission denied: $reason.")


class NotFoundHTTPException(BaseClientHTTPException):
    """Not found 404 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 for more information.
    """

    status_code = status.HTTP_404_NOT_FOUND
    type_ = "not_found"
    message = "Entity not found."
    template = Template("$entity not found.")


class MethodNotAllowedHTTPException(BaseClientHTTPException):
    """Method not allowed 405 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/405 for more information.
    """

    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    type_ = "method_not_allowed"
    message = "Method not allowed."
    template = Template("Method $method not allowed.")


class NotAcceptableHTTPException(BaseClientHTTPException):
    """Not acceptable 406 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/406 for more information.
    """

    status_code = status.HTTP_406_NOT_ACCEPTABLE
    type_ = "not_acceptable"
    message = "No content found that conforms to the given criteria."
    template = Template("No content found that conforms to the given criteria: $reason.")


class ProxyAuthenticationRequiredHTTPException(BaseClientHTTPException):
    """Proxy Authentication Required 407 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/407 for more information.
    """

    status_code = status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED
    type_ = "proxy_authentication_required"
    message = "User should be authenticated by proxy."
    template = Template("User should be authenticated by proxy: $reason.")


class RequestTimeoutHTTPException(BaseClientHTTPException):
    """Proxy Authentication Required 408 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/408 for more information.
    """

    status_code = status.HTTP_408_REQUEST_TIMEOUT
    type_ = "request_timeout"
    message = "Request timeout."
    template = Template("Request timeout: $reason.")


class ConflictHTTPException(BaseClientHTTPException):
    """Conflict 409 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/409 for more information.
    """

    status_code = status.HTTP_409_CONFLICT
    type_ = "conflict"
    message = "Request conflict with the current state of the server."
    template = Template("Request conflict with the current state of the server: $reason.")


class GoneHTTPException(BaseClientHTTPException):
    """Gone 410 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/410 for more information.
    """

    status_code = status.HTTP_410_GONE
    type_ = "gone"
    message = "Requested content has been permanently deleted from server."
    template = Template("Requested content has been permanently deleted from server: $reason.")


class LengthRequiredHTTPException(BaseClientHTTPException):
    """Length required 411 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/411 for more information.
    """

    status_code = status.HTTP_411_LENGTH_REQUIRED
    type_ = "length_required"
    message = "No Content-Length header was provided."
    template = Template("No Content-Length header was provided: $reason.")


class PreconditionFailedHTTPException(BaseClientHTTPException):
    """Precondition failed 412 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/412 for more information.
    """

    status_code = status.HTTP_412_PRECONDITION_FAILED
    type_ = "precondition_failed"
    message = "Access to the target resource was denied due to incorrect condition."
    template = Template(
        "Access to the target resource was denied due to incorrect condition: $reason.",
    )


class PayloadTooLargeHTTPException(BaseClientHTTPException):
    """Payload too large 413 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/413 for more information.
    """

    status_code = status.HTTP_413_PAYLOAD_TOO_LARGE
    type_ = "payload_too_large"
    message = "Request entity is larger than limits defined by server."
    template = Template("Request entity is larger than limits defined by server: $reason.")


class UriTooLongHTTPException(BaseClientHTTPException):
    """URI too long 414 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/414 for more information.
    """

    status_code = status.HTTP_414_URI_TOO_LONG
    type_ = "uri_too_long"
    message = "The requested URI is longer than the server is willing to interpret."
    template = Template(
        "The requested URI is longer than the server is willing to interpret: $reason.",
    )


class UnsupportedMediaTypeHTTPException(BaseClientHTTPException):
    """Unsupported media type 415 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/415 for more information.
    """

    status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    type_ = "unsupported_media_type"
    message = "Request data incorrect media format."
    template = Template("Request data incorrect media format: $reason.")


class RangeNotSatisfiableHTTPException(BaseClientHTTPException):
    """Range not satisfiable 416 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/416 for more information.
    """

    status_code = status.HTTP_416_RANGE_NOT_SATISFIABLE
    type_ = "range_not_satisfiable"
    message = "Request Range header is outside the size of the target URI's data."
    template = Template(
        "Request Range header is outside the size of the target URI's data: $reason.",
    )


class ExpectationFailedHTTPException(BaseClientHTTPException):
    """Expectation failed 417 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/417 for more information.
    """

    status_code = status.HTTP_417_EXPECTATION_FAILED
    type_ = "expectation_failed"
    message = (
        "The expectation indicated by the Expect request header field cannot be met by the server."
    )
    template = Template(
        (
            "the expectation indicated by the Expect request header "
            "field cannot be met by the server: $reason."
        ),
    )


class ImATeapotHTTPException(BaseClientHTTPException):
    """Expectation failed 418 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/418 for more information.
    """

    status_code = status.HTTP_418_IM_A_TEAPOT
    type_ = "im_a_teapot"
    message = "I'm a teapot."
    template = Template("I'm a teapot: $reason.")


class MisdirectedRequestHTTPException(BaseClientHTTPException):
    """Misdirected request 421 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/421 for more information.
    """

    status_code = status.HTTP_421_MISDIRECTED_REQUEST
    type_ = "misdirected_request"
    message = "The request was directed at a server that is not able to produce a response."
    template = Template(
        "The request was directed at a server that is not able to produce a response: $reason.",
    )


class UnprocessableContentHTTPException(BaseClientHTTPException):
    """Misdirected request 422 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/422 for more information.
    """

    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    type_ = "unprocessable_content"
    message = "The request was well-formed but was unable to be followed due to semantic errors."
    template = Template(
        (
            "The request was well-formed but was unable to be "
            "followed due to semantic errors: $reason."
        ),
    )


class LockedHTTPException(BaseClientHTTPException):
    """Locked 423 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/423 for more information.
    """

    status_code = status.HTTP_423_LOCKED
    type_ = "locked"
    message = "The resource that is being accessed is locked."
    template = Template("The resource that is being accessed is locked: $reason.")


class FailedDependencyHTTPException(BaseClientHTTPException):
    """Failed dependency 424 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/424 for more information.
    """

    status_code = status.HTTP_424_FAILED_DEPENDENCY
    type_ = "failed_dependency"
    message = "The request failed due to failure of a previous request."
    template = Template("The request failed due to failure of a previous request: $reason.")


class TooEarlyHTTPException(BaseClientHTTPException):
    """Too early 425 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/425 for more information.
    """

    status_code = status.HTTP_425_TOO_EARLY
    type_ = "too_early"
    message = "Too dangerous to process request. Try again later."
    template = Template("Too dangerous to process request: $reason. Try again later.")


class UpgradeRequiredHTTPException(BaseClientHTTPException):
    """Upgrade required 426 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/426 for more information.
    """

    status_code = status.HTTP_426_UPGRADE_REQUIRED
    type_ = "upgrade_required"
    message = "Upgrade protocol required."
    template = Template("Upgrade protocol required: $reason.")


class PreconditionRequiredHTTPException(BaseClientHTTPException):
    """Precondition required 428 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/428 for more information.
    """

    status_code = status.HTTP_428_PRECONDITION_REQUIRED
    type_ = "precondition_required"
    message = "Conditional request required."
    template = Template("Conditional request required: $reason.")


class TooManyRequestsHTTPException(BaseClientHTTPException):
    """Too many requests 429 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429 for more information.
    """

    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    type_ = "too_many_requests"
    message = "Too many requests sent in a given amount of time."
    template = Template("Too many requests sent in a given amount of time: $reason.")


class RequestHeaderFieldsTooLargeHTTPException(BaseClientHTTPException):
    """Too many requests 431 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/431 for more information.
    """

    status_code = status.HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE
    type_ = "request_header_fields_too_large"
    message = "Request header fields too large."
    template = Template("Request header fields too large: $reason.")


class UnavailableForLegalReasonHTTPException(BaseClientHTTPException):
    """Unavailable for legal reason 451 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/451 for more information.
    """

    status_code = status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
    type_ = "unavailable_for_legal_reason"
    message = "Resource cannot legally be provided."
    template = Template("Resource cannot legally be provided: $reason.")
