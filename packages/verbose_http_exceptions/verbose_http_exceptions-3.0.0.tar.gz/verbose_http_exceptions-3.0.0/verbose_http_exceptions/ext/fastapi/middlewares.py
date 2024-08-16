from typing import TYPE_CHECKING

from fastapi.responses import JSONResponse

from verbose_http_exceptions import status
from verbose_http_exceptions.exc.server_error import InternalServerErrorHTTPException

if TYPE_CHECKING:
    from fastapi import Request, Response
    from starlette.middleware.base import RequestResponseEndpoint


async def python_errors_handling_middleware(
    request: "Request",
    call_next: "RequestResponseEndpoint",
) -> "Response":
    """Handle any non-HTTP exception."""
    try:
        return await call_next(request)
    except Exception as exc:  # noqa: BLE001
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=InternalServerErrorHTTPException(message=str(exc)).as_dict(),
        )
