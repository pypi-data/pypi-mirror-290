__all__ = (
    "HTTP_100_CONTINUE",
    "HTTP_101_SWITCHING_PROTOCOLS",
    "HTTP_102_PROCESSING",
    "HTTP_103_EARLY_HINTS",
    "HTTP_200_OK",
    "HTTP_201_CREATED",
    "HTTP_202_ACCEPTED",
    "HTTP_203_NON_AUTHORITATIVE_INFORMATION",
    "HTTP_204_NO_CONTENT",
    "HTTP_205_RESET_CONTENT",
    "HTTP_206_PARTIAL_CONTENT",
    "HTTP_207_MULTI_STATUS",
    "HTTP_208_ALREADY_REPORTED",
    "HTTP_226_IM_USED",
    "HTTP_300_MULTIPLE_CHOICES",
    "HTTP_301_MOVED_PERMANENTLY",
    "HTTP_302_FOUND",
    "HTTP_303_SEE_OTHER",
    "HTTP_304_NOT_MODIFIED",
    "HTTP_305_USE_PROXY",
    "HTTP_306_UNUSED",
    "HTTP_307_TEMPORARY_REDIRECT",
    "HTTP_308_PERMANENT_REDIRECT",
    "HTTP_400_BAD_REQUEST",
    "HTTP_401_UNAUTHORIZED",
    "HTTP_402_PAYMENT_REQUIRED",
    "HTTP_403_FORBIDDEN",
    "HTTP_404_NOT_FOUND",
    "HTTP_405_METHOD_NOT_ALLOWED",
    "HTTP_406_NOT_ACCEPTABLE",
    "HTTP_407_PROXY_AUTHENTICATION_REQUIRED",
    "HTTP_408_REQUEST_TIMEOUT",
    "HTTP_409_CONFLICT",
    "HTTP_410_GONE",
    "HTTP_411_LENGTH_REQUIRED",
    "HTTP_412_PRECONDITION_FAILED",
    "HTTP_413_PAYLOAD_TOO_LARGE",
    "HTTP_414_URI_TOO_LONG",
    "HTTP_415_UNSUPPORTED_MEDIA_TYPE",
    "HTTP_416_RANGE_NOT_SATISFIABLE",
    "HTTP_417_EXPECTATION_FAILED",
    "HTTP_418_IM_A_TEAPOT",
    "HTTP_421_MISDIRECTED_REQUEST",
    "HTTP_422_UNPROCESSABLE_CONTENT",
    "HTTP_423_LOCKED",
    "HTTP_424_FAILED_DEPENDENCY",
    "HTTP_425_TOO_EARLY",
    "HTTP_426_UPGRADE_REQUIRED",
    "HTTP_428_PRECONDITION_REQUIRED",
    "HTTP_429_TOO_MANY_REQUESTS",
    "HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE",
    "HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS",
    "HTTP_500_INTERNAL_SERVER_ERROR",
    "HTTP_501_NOT_IMPLEMENTED",
    "HTTP_502_BAD_GATEWAY",
    "HTTP_503_SERVICE_UNAVAILABLE",
    "HTTP_504_GATEWAY_TIMEOUT",
    "HTTP_505_HTTP_VERSION_NOT_SUPPORTED",
    "HTTP_506_VARIANT_ALSO_NEGOTIATES",
    "HTTP_507_INSUFFICIENT_STORAGE",
    "HTTP_508_LOOP_DETECTED",
    "HTTP_510_NOT_EXTENDED",
    "HTTP_511_NETWORK_AUTHENTICATION_REQUIRED",
    "WS_1000_NORMAL_CLOSURE",
    "WS_1001_GOING_AWAY",
    "WS_1002_PROTOCOL_ERROR",
    "WS_1003_UNSUPPORTED_DATA",
    "WS_1004_RESERVED",
    "WS_1005_NO_STATUS_RCVD",
    "WS_1006_ABNORMAL_CLOSURE",
    "WS_1007_INVALID_FRAME_PAYLOAD_DATA",
    "WS_1008_POLICY_VIOLATION",
    "WS_1009_MESSAGE_TOO_BIG",
    "WS_1010_MANDATORY_EXT",
    "WS_1011_INTERNAL_ERROR",
    "WS_1012_SERVICE_RESTART",
    "WS_1013_TRY_AGAIN_LATER",
    "WS_1014_BAD_GATEWAY",
    "WS_1015_TLS_HANDSHAKE",
)


HTTP_100_CONTINUE = 100
"""
This interim response indicates that the client should continue the request or ignore the response
if the request is already finished.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_101_SWITCHING_PROTOCOLS = 101
"""
This code is sent in response to an `Upgrade` request header from the client and indicates the
protocol the server is switching to.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
Upgrade header: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Upgrade
"""
HTTP_102_PROCESSING = 102
"""
This code indicates that the server has received and is processing the request, but no response
is available yet.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_103_EARLY_HINTS = 103
"""
This status code is primarily intended to be used with the `Link` header, letting the user agent
start preloading resources while the server prepares a response or preconnect to an origin from
which the page will need resources.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
Link header: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Link
"""
HTTP_200_OK = 200
"""
The request succeeded. The result meaning of "success" depends on the HTTP method:

- `GET`: The resource has been fetched and transmitted in the message body.
- `HEAD`: The representation headers are included in the response without any message body.
- `PUT` or `POST`: The resource describing the result of the action is transmitted in the message
  body.
- `TRACE`: The message body contains the request message as received by the server.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_201_CREATED = 201
"""
The request succeeded, and a new resource was created as a result. This is typically the response
sent after `POST` requests, or some `PUT` requests.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_202_ACCEPTED = 202
"""
The request has been received but not yet acted upon. It is noncommittal, since there is no way
in HTTP to later send an asynchronous response indicating the outcome of the request. It is
intended for cases where another process or server handles the request, or for batch processing.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_203_NON_AUTHORITATIVE_INFORMATION = 203
"""
This response code means the returned metadata is not exactly the same as is available from the
origin server, but is collected from a local or a third-party copy. This is mostly used for
mirrors or backups of another resource. Except for that specific case, the `200 OK` response is
preferred to this status.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_204_NO_CONTENT = 204
"""
There is no content to send for this request, but the headers may be useful. The user agent may
update its cached headers for this resource with the new ones.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_205_RESET_CONTENT = 205
"""
Tells the user agent to reset the document which sent this request.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_206_PARTIAL_CONTENT = 206
"""
This response code is used when the `Range` header is sent from the client to request only part of
a resource.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
Range header: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Range
"""
HTTP_207_MULTI_STATUS = 207
"""
Conveys information about multiple resources, for situations where multiple status codes might
be appropriate.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_208_ALREADY_REPORTED = 208
"""
Used inside a `<dav:propstat>` response element to avoid repeatedly enumerating the internal
members of multiple bindings to the same collection.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_226_IM_USED = 226
"""
The server has fulfilled a `GET` request for the resource, and the response is a representation of
the result of one or more instance-manipulations applied to the current instance.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_300_MULTIPLE_CHOICES = 300
"""
The request has more than one possible response. The user agent or user should choose one of them.
(There is no standardized way of choosing one of the responses, but HTML links to the
possibilities are recommended so the user can pick.)

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_301_MOVED_PERMANENTLY = 301
"""
The URL of the requested resource has been changed permanently. The new URL is given
in the response.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_302_FOUND = 302
"""
This response code means that the URI of requested resource has been changed temporarily.
Further changes in the URI might be made in the future. Therefore, this same URI should be
used by the client in future requests.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_303_SEE_OTHER = 303
"""
The server sent this response to direct the client to get the requested resource at another URI
with a `GET` request.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_304_NOT_MODIFIED = 304
"""
This is used for caching purposes. It tells the client that the response has not been modified,
so the client can continue to use the same cached version of the response.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_305_USE_PROXY = 305
"""
DEPRECATED. Not for use in websites.
------------------------------------

Defined in a previous version of the HTTP specification to indicate that a requested response
must be accessed by a proxy. It has been deprecated due to security concerns regarding in-band
configuration of a proxy.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_306_UNUSED = 306
"""
This response code is no longer used; it is just reserved. It was used in a previous version of
the HTTP/1.1 specification.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_307_TEMPORARY_REDIRECT = 307
"""
The server sends this response to direct the client to get the requested resource at another URI
with the same method that was used in the prior request. This has the same semantics as the `302
Found` HTTP response code, with the exception that the user agent must not change the HTTP method
used: if a `POST` was used in the first request, a `POST` must be used in the second request.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_308_PERMANENT_REDIRECT = 308
"""
This means that the resource is now permanently located at another URI, specified by the
`Location`: HTTP Response header. This has the same semantics as the `301 Moved Permanently`
HTTP response code, with the exception that the user agent must not change the HTTP method
used: if a `POST` was used in the first request, a `POST` must be used in the second request.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
Location header: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Location
"""
HTTP_400_BAD_REQUEST = 400
"""
The server cannot or will not process the request due to something that is perceived to be a
client error (e.g., malformed request syntax, invalid request message framing, or deceptive
request routing).

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_401_UNAUTHORIZED = 401
"""
Although the HTTP standard specifies "unauthorized", semantically this response means
"unauthenticated". That is, the client must authenticate itself to get the requested response.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_402_PAYMENT_REQUIRED = 402
"""
EXPERIMENTAL. Expect behavior to change in the future.
------------------------------------------------------

This response code is reserved for future use. The initial aim for creating this code was
using it for digital payment systems, however this status code is used very rarely and no
standard convention exists.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_403_FORBIDDEN = 403
"""
The client does not have access rights to the content; that is, it is unauthorized, so the
server is refusing to give the requested resource. Unlike `401 Unauthorized`, the client's
identity is known to the server.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_404_NOT_FOUND = 404
"""
The server cannot find the requested resource. In the browser, this means the URL is not
recognized. In an API, this can also mean that the endpoint is valid but the resource itself
does not exist. Servers may also send this response instead of `403 Forbidden` to hide the
existence of a resource from an unauthorized client. This response code is probably the most
well known due to its frequent occurrence on the web.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_405_METHOD_NOT_ALLOWED = 405
"""
The request method is known by the server but is not supported by the target resource. For
example, an API may not allow calling `DELETE` to remove a resource.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_406_NOT_ACCEPTABLE = 406
"""
This response is sent when the web server, after performing server-driven content
negotiation, doesn't find any content that conforms to the criteria given by the user agent.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
server-driven content negotiation info: https://developer.mozilla.org/en-US/docs/Web/HTTP/Content_negotiation#server-driven_content_negotiation
"""
HTTP_407_PROXY_AUTHENTICATION_REQUIRED = 407
"""
This is similar to `401 Unauthorized` but authentication is needed to be done by a proxy.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_408_REQUEST_TIMEOUT = 408
"""
This response is sent on an idle connection by some servers, even without any previous request
by the client. It means that the server would like to shut down this unused connection. This
response is used much more since some browsers, like Chrome, Firefox 27+, or IE9, use HTTP
pre-connection mechanisms to speed up surfing. Also note that some servers merely shut down
the connection without sending this message.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_409_CONFLICT = 409
"""
This response is sent when a request conflicts with the current state of the server.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_410_GONE = 410
"""
This response is sent when the requested content has been permanently deleted from server,
with no forwarding address. Clients are expected to remove their caches and links to the
resource. The HTTP specification intends this status code to be used for "limited-time,
promotional services". APIs should not feel compelled to indicate resources that have been
deleted with this status code.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_411_LENGTH_REQUIRED = 411
"""
Server rejected the request because the `Content-Length` header field is not defined
and the server requires it.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
Content-Length header: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Length
"""
HTTP_412_PRECONDITION_FAILED = 412
"""
The client has indicated preconditions in its headers which the server does not meet.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_413_PAYLOAD_TOO_LARGE = 413
"""
Request entity is larger than limits defined by server. The server might close the connection
or return an `Retry-After` header field.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
Retry-After header: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Retry-After
"""
HTTP_414_URI_TOO_LONG = 414
"""
The URI requested by the client is longer than the server is willing to interpret.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_415_UNSUPPORTED_MEDIA_TYPE = 415
"""
The media format of the requested data is not supported by the server, so the server is
rejecting the request.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_416_RANGE_NOT_SATISFIABLE = 416
"""
The range specified by the `Range` header field in the request cannot be fulfilled. It's
possible that the range is outside the size of the target URI's data.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
Range header: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Range
"""
HTTP_417_EXPECTATION_FAILED = 417
"""
This response code means the expectation indicated by the `Expect` request header field cannot
be met by the server.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
Expect header: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Expect
"""
HTTP_418_IM_A_TEAPOT = 418
"""
The server refuses the attempt to brew coffee with a teapot.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
Joke explanation: https://en.wikipedia.org/wiki/Hyper_Text_Coffee_Pot_Control_Protocol
"""
HTTP_421_MISDIRECTED_REQUEST = 421
"""
The request was directed at a server that is not able to produce a response. This can be sent
by a server that is not configured to produce responses for the combination of scheme and
authority that are included in the request URI.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_422_UNPROCESSABLE_CONTENT = 422
"""
The request was well-formed but was unable to be followed due to semantic errors.

Used in FastAPI as default status code for request validation error.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
FastAPI docs: https://fastapi.tiangolo.com/tutorial/handling-errors/#override-request-validation-exceptions
"""
HTTP_423_LOCKED = 423
"""
The resource that is being accessed is locked.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_424_FAILED_DEPENDENCY = 424
"""
The request failed due to failure of a previous request.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_425_TOO_EARLY = 425
"""
Indicates that the server is unwilling to risk processing a request that might be replayed.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_426_UPGRADE_REQUIRED = 426
"""
The server refuses to perform the request using the current protocol but might be willing to
do so after the client upgrades to a different protocol. The server sends an `Upgrade` header in
a 426 response to indicate the required protocol(s).

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
Upgrade header: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Upgrade
"""
HTTP_428_PRECONDITION_REQUIRED = 428
"""
The origin server requires the request to be conditional. This response is intended to prevent
the 'lost update' problem, where a client `GET`s a resource's state, modifies it and `PUT`s it
back to the server, when meanwhile a third party has modified the state on the server, leading
to a conflict.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_429_TOO_MANY_REQUESTS = 429
"""
The user has sent too many requests in a given amount of time ("rate limiting").

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE = 431
"""
The server is unwilling to process the request because its header fields are too large.
The request may be resubmitted after reducing the size of the request header fields.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS = 451
"""
The user agent requested a resource that cannot legally be provided, such as a web page
censored by a government.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_500_INTERNAL_SERVER_ERROR = 500
"""
The server has encountered a situation it does not know how to handle.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_501_NOT_IMPLEMENTED = 501
"""
The request method is not supported by the server and cannot be handled. The only methods
that servers are required to support (and therefore that must not return this code) are
`GET` and `HEAD`.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_502_BAD_GATEWAY = 502
"""
This error response means that the server, while working as a gateway to get a response
needed to handle the request, got an invalid response.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_503_SERVICE_UNAVAILABLE = 503
"""
The server is not ready to handle the request. Common causes are a server that is down for
maintenance or that is overloaded. Note that together with this response, a user-friendly
page explaining the problem should be sent. This response should be used for temporary
conditions and the `Retry-After` HTTP header should, if possible, contain the estimated time
before the recovery of the service. The webmaster must also take care about the
caching-related headers that are sent along with this response, as these temporary condition
responses should usually not be cached.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
Retry-After header: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Retry-After
"""
HTTP_504_GATEWAY_TIMEOUT = 504
"""
This error response is given when the server is acting as a gateway and cannot get a
response in time.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_505_HTTP_VERSION_NOT_SUPPORTED = 505
"""
The HTTP version used in the request is not supported by the server.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_506_VARIANT_ALSO_NEGOTIATES = 506
"""
The server has an internal configuration error: the chosen variant resource is configured to
engage in transparent content negotiation itself, and is therefore not a proper end point in
the negotiation process.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_507_INSUFFICIENT_STORAGE = 507
"""
The method could not be performed on the resource because the server is unable to store the
representation needed to successfully complete the request.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_508_LOOP_DETECTED = 508
"""
The server detected an infinite loop while processing the request.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_510_NOT_EXTENDED = 510
"""
Further extensions to the request are required for the server to fulfill it.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
HTTP_511_NETWORK_AUTHENTICATION_REQUIRED = 511
"""
Indicates that the client needs to authenticate to gain network access.

Information from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
"""
WS_1000_NORMAL_CLOSURE = 1000
"""
The connection successfully completed the purpose for which it was created.

Information from https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent/code
"""
WS_1001_GOING_AWAY = 1001
"""
The endpoint is going away, either because of a server failure or because the browser
is navigating away from the page that opened the connection.

Information from https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent/code
"""
WS_1002_PROTOCOL_ERROR = 1002
"""
The endpoint is terminating the connection due to a protocol error.

Information from https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent/code
"""
WS_1003_UNSUPPORTED_DATA = 1003
"""
The connection is being terminated because the endpoint received data of a type it cannot
accept. (For example, a text-only endpoint received binary data.)

Information from https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent/code
"""
WS_1004_RESERVED = 1004
"""
`Reserved`. A meaning might be defined in the future.

Information from https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent/code
"""
WS_1005_NO_STATUS_RCVD = 1005
"""
`Reserved`. Indicates that no status code was provided even though one was expected.

Information from https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent/code
"""
WS_1006_ABNORMAL_CLOSURE = 1006
"""
`Reserved`. Indicates that a connection was closed abnormally (that is, with no close frame
being sent) when a status code is expected.

Information from https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent/code
"""
WS_1007_INVALID_FRAME_PAYLOAD_DATA = 1007
"""
The endpoint is terminating the connection because a message was received that contained
inconsistent data (e.g., non-UTF-8 data within a text message).

Information from https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent/code
"""
WS_1008_POLICY_VIOLATION = 1008
"""
The endpoint is terminating the connection because it received a message that violates its
policy. This is a generic status code, used when codes 1003 and 1009 are not suitable.

Information from https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent/code
"""
WS_1009_MESSAGE_TOO_BIG = 1009
"""
The endpoint is terminating the connection because a data frame was received that is too large.

Information from https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent/code
"""
WS_1010_MANDATORY_EXT = 1010
"""
The client is terminating the connection because it expected the server to negotiate one
or more extension, but the server didn't.

Information from https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent/code
"""
WS_1011_INTERNAL_ERROR = 1011
"""
The server is terminating the connection because it encountered an unexpected condition
that prevented it from fulfilling the request.

Information from https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent/code
"""
WS_1012_SERVICE_RESTART = 1012
"""
The server is terminating the connection because it is restarting.

Information from https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent/code
"""
WS_1013_TRY_AGAIN_LATER = 1013
"""
The server is terminating the connection due to a temporary condition, e.g. it is overloaded
and is casting off some of its clients.

Information from https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent/code
"""
WS_1014_BAD_GATEWAY = 1014
"""
The server was acting as a gateway or proxy and received an invalid response from the
upstream server. This is similar to 502 HTTP Status Code.

Information from https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent/code
"""
WS_1015_TLS_HANDSHAKE = 1015
"""
Reserved. Indicates that the connection was closed due to a failure to perform a TLS
handshake (e.g., the server certificate can't be verified).

Information from https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent/code
"""


def __dir__() -> list[str]:
    return sorted(__all__)
