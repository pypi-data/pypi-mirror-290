from verbose_http_exceptions import status
from verbose_http_exceptions.exc.base import BaseVerboseHTTPException


class BaseRedirectionHTTPException(BaseVerboseHTTPException):
    """Base redirect verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#redirection_messages for more
    information.
    """

    __skip_abstract_raise_error__ = True

    code = "redirect"


class MultipleChoicesHTTPException(BaseRedirectionHTTPException):
    """Multiple choices 300 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/300 for more information.
    """

    status_code = status.HTTP_300_MULTIPLE_CHOICES
    type_ = "multiple_choices"
    message = "The request has more than one possible response."


class MovedPermanentlyHTTPException(BaseRedirectionHTTPException):
    """Moved permanently 301 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/301 for more information.
    """

    status_code = status.HTTP_301_MOVED_PERMANENTLY
    type_ = "moved_permanently"
    message = "The URL of the requested resource has been changed permanently."


class FoundHTTPException(BaseRedirectionHTTPException):
    """Found 302 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/302 for more information.
    """

    status_code = status.HTTP_302_FOUND
    type_ = "found"
    message = "The URI of requested resource has been temporarily changed."


class SeeOtherHTTPException(BaseRedirectionHTTPException):
    """See other 303 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/303 for more information.
    """

    status_code = status.HTTP_303_SEE_OTHER
    type_ = "see_other"
    message = "Get the requested resource at another URI."


class NotModifiedHTTPException(BaseRedirectionHTTPException):
    """Not modified 304 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/304 for more information.
    """

    status_code = status.HTTP_304_NOT_MODIFIED
    type_ = "not_modified"
    message = (
        "The response has not been modified, so you can continue "
        "to use the same cached version of the response."
    )


class UseProxyHTTPException(BaseRedirectionHTTPException):
    """Use proxy 305 verbose HTTP response class.

    Deprecated status code.
    """

    status_code = status.HTTP_305_USE_PROXY
    type_ = "use_proxy"
    message = "The requested response must be accessed by a proxy."


class UnusedHTTPException(BaseRedirectionHTTPException):
    """Use proxy 306 verbose HTTP response class.

    This response code is no longer used; it is just reserved. It was used in a previous
    version of the HTTP/1.1 specification.
    """

    status_code = status.HTTP_306_UNUSED
    type_ = "unused"
    message = "Unused method with unused message."


class TemporaryRedirectHTTPException(BaseRedirectionHTTPException):
    """Temporary redirect 307 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/307 for more information.
    """

    status_code = status.HTTP_307_TEMPORARY_REDIRECT
    type_ = "temporary_redirect"
    message = "Temporary redirect to another URI."


class PermanentRedirectHTTPException(BaseRedirectionHTTPException):
    """Permanent redirect 308 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/308 for more information.
    """

    status_code = status.HTTP_308_PERMANENT_REDIRECT
    type_ = "permanent_redirect"
    message = "Permanent redirect to another URI."
