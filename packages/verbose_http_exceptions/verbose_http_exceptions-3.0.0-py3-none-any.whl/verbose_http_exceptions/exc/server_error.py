from string import Template

from verbose_http_exceptions import status
from verbose_http_exceptions.exc.base import BaseVerboseHTTPException


class BaseServerHTTPException(BaseVerboseHTTPException):
    """Base server error HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#server_error_responses for more
    information.
    """

    __skip_abstract_raise_error__ = True

    code = "server_error"


class InternalServerErrorHTTPException(BaseServerHTTPException):
    """Internal server error 500 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500 for more information.
    """

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    type_ = "internal_server_error"
    message = "Internal server error was found."
    template = Template("Internal server error was found: $reason.")


class NotImplementedHTTPException(BaseServerHTTPException):
    """Not implemented 501 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/501 for more information.
    """

    status_code = status.HTTP_501_NOT_IMPLEMENTED
    type_ = "not_implemented"
    message = "The request method is not supported and cannot be handled."
    template = Template("The request method is not supported and cannot be handled: $reason.")


class BadGatewayHTTPException(BaseServerHTTPException):
    """Bad gateway 502 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/502 for more information.
    """

    status_code = status.HTTP_502_BAD_GATEWAY
    type_ = "bad_gateway"
    message = "Gateway error."
    template = Template("Gateway error: $reason.")


class ServiceUnavailableHTTPException(BaseServerHTTPException):
    """Service unavailable 503 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/503 for more information.
    """

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    type_ = "service_unavailable"
    message = "The server is not ready to handle the request."
    template = Template("The server is not ready to handle the request: $reason.")


class GatewayTimeoutHTTPException(BaseServerHTTPException):
    """Gateway timeout 504 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/504 for more information.
    """

    status_code = status.HTTP_504_GATEWAY_TIMEOUT
    type_ = "gateway_timeout"
    message = "The server is acting as a gateway and cannot get a response in time."
    template = Template(
        "The server is acting as a gateway and cannot get a response in time: $reason.",
    )


class VersionNotSupportedHTTPException(BaseServerHTTPException):
    """Version not supported 505 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/505 for more information.
    """

    status_code = status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED
    type_ = "http_version_not_supported"
    message = "The HTTP version used in the request is not supported by the server."
    template = Template(
        "The HTTP version used in the request is not supported by the server: $reason.",
    )


class VariantAlsoNegotiatesHTTPException(BaseServerHTTPException):
    """Variant also negotiates 506 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/506 for more information.
    """

    status_code = status.HTTP_506_VARIANT_ALSO_NEGOTIATES
    type_ = "variant_also_negotiates"
    # NOTE: IDK, how to make it short
    message = (
        "The server has an internal configuration error: the chosen variant resource is "
        "configured to engage in transparent content negotiation itself, and is therefore "
        "not a proper end point in the negotiation process."
    )
    template = Template(
        (
            "The server has an internal configuration error: the chosen variant resource is "
            "configured to engage in transparent content negotiation itself, and is therefore "
            "not a proper end point in the negotiation process: $reason."
        ),
    )


class InsufficientStorageHTTPException(BaseServerHTTPException):
    """Insufficient storage 507 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/507 for more information.
    """

    status_code = status.HTTP_507_INSUFFICIENT_STORAGE
    type_ = "insufficient_storage"
    message = (
        "The server is unable to store the representation needed "
        "to successfully complete the request."
    )
    template = Template(
        (
            "The server is unable to store the representation needed "
            "to successfully complete the request: $reason."
        ),
    )


class LoopDetectedHTTPException(BaseServerHTTPException):
    """Loop detected 508 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/508 for more information.
    """

    status_code = status.HTTP_508_LOOP_DETECTED
    type_ = "loop_detected"
    message = "The server detected an infinite loop while processing the request."
    template = Template(
        "The server detected an infinite loop while processing the request: $reason.",
    )


class NotExtendedHTTPException(BaseServerHTTPException):
    """Not extended 510 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/510 for more information.
    """

    status_code = status.HTTP_510_NOT_EXTENDED
    type_ = "not_extended"
    message = "Further extensions to the request are required for the server to fulfill it."
    template = Template(
        "Further extensions to the request are required for the server to fulfill it: $reason.",
    )


class NetworkAuthenticationRequiredHTTPException(BaseServerHTTPException):
    """Not extended 511 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/511 for more information.
    """

    status_code = status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED
    type_ = "network_authentication_required"
    message = "Network authentication required."
    template = Template("Network authentication required: $reason.")
