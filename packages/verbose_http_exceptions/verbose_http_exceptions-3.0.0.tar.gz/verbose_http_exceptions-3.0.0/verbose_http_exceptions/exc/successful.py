from verbose_http_exceptions import status
from verbose_http_exceptions.exc.base import BaseVerboseHTTPException


class BaseSuccessfulHTTPException(BaseVerboseHTTPException):
    """Base success verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#successful_responses for more
    information.
    """

    __skip_abstract_raise_error__ = True

    code = "success"


class OkHTTPException(BaseSuccessfulHTTPException):
    """Ok 200 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/200 for more information.
    """

    status_code = status.HTTP_200_OK
    type_ = "ok"
    message = "The request succeeded."


class CreatedHTTPException(BaseSuccessfulHTTPException):
    """Created 201 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/201 for more information.
    """

    status_code = status.HTTP_201_CREATED
    type_ = "created"
    message = "The request succeeded, and a new resource was created as a result."


class AcceptedHTTPException(BaseSuccessfulHTTPException):
    """Created 202 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/202 for more information.
    """

    status_code = status.HTTP_202_ACCEPTED
    type_ = "created"
    message = "The request has been received but not yet acted upon."


class NonAuthoritativeInformationHTTPException(BaseSuccessfulHTTPException):
    """Non-Authoritative Information 203 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/203 for more information.
    """

    status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
    type_ = "not_same_metadata"
    message = "Returned metadata is not exactly the same as is available from the origin server."


# NOTE: There is no "No content" http exception because of itself - it can't contains any content.


class ResetContentHTTPException(BaseSuccessfulHTTPException):
    """Reset content 205 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/205 for more information.
    """

    status_code = status.HTTP_205_RESET_CONTENT
    type_ = "reset_content"
    message = "Reset the document which sent this request."


class PartialContentHTTPException(BaseSuccessfulHTTPException):
    """Partial content 206 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/206 for more information.
    """

    status_code = status.HTTP_206_PARTIAL_CONTENT
    type_ = "partial_content"
    message = "Partial content sent due to Range header passed."


class MultiStatusHTTPException(BaseSuccessfulHTTPException):
    """Multi-Status 207 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/207 for more information.
    """

    status_code = status.HTTP_207_MULTI_STATUS
    type_ = "multi_status"
    message = "Multiple status codes were appropriated."


class AlreadyReportedHTTPException(BaseSuccessfulHTTPException):
    """Already reported 208 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/208 for more information.
    """

    status_code = status.HTTP_208_ALREADY_REPORTED
    type_ = "already_reported"
    message = (
        "Avoid repeatedly enumerating the internal members"
        "of multiple bindings to the same collection."
    )


class IMUsedHTTPException(BaseSuccessfulHTTPException):
    """IM used 226 verbose HTTP response class.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/226 for more information.
    """

    status_code = status.HTTP_226_IM_USED
    type_ = "im_used"
    message = "Delta returned."
