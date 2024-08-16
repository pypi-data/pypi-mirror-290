from verbose_http_exceptions import status
from verbose_http_exceptions.exc.base import BaseVerboseHTTPException


class BaseInformationalHTTPException(BaseVerboseHTTPException):
    """Base informational HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#information_responses for more
    information.
    """

    __skip_abstract_raise_error__ = True

    code = "info"


class ContinueHTTPException(BaseInformationalHTTPException):
    """Continue 100 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/100 for more information.
    """

    status_code = status.HTTP_100_CONTINUE
    type_ = "continue"
    message = (
        "Client should continue the request"
        "or ignore the response if the request is already finished."
    )


class SwitchingProtocolsHTTPException(BaseInformationalHTTPException):
    """Switching Protocols 101 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/101 for more information.
    """

    status_code = status.HTTP_101_SWITCHING_PROTOCOLS
    type_ = "switching_protocol"
    message = "Server has switched to other protocol (see Update header)."


class ProcessingHTTPException(BaseInformationalHTTPException):
    """Processing 102 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/102 for more information.
    """

    status_code = status.HTTP_102_PROCESSING
    type_ = "switching_protocol"
    message = "Server has received and is processing the request, but no response is available yet."


class EarlyHintsHTTPException(BaseInformationalHTTPException):
    """Early hints 103 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/103 for more information.
    """

    status_code = status.HTTP_103_EARLY_HINTS
    type_ = "early_hints"
    message = "Server is preloading resources. Go to resource in Link header."
