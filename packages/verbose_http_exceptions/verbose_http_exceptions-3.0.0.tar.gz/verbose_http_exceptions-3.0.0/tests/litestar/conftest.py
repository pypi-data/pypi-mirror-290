from typing import TYPE_CHECKING, Literal

import pytest
from litestar import Litestar, get
from litestar import status_codes as status
from litestar.exceptions import HTTPException, ValidationException
from litestar.testing import TestClient

from verbose_http_exceptions.exc.base import BaseVerboseHTTPException
from verbose_http_exceptions.exc.server_error import InternalServerErrorHTTPException
from verbose_http_exceptions.ext.litestar.handlers import (
    any_http_exception_handler,
    python_error_handler,
    verbose_http_exception_handler,
    verbose_request_validation_error_handler,
)

if TYPE_CHECKING:
    from verbose_http_exceptions.ext.litestar.types import (
        ValidationAttrFindType,
        ValidationLocationFindType,
        ValidationTypeFindType,
    )


@pytest.fixture()
def test_app_only_verbose():  # noqa: ANN201
    @get("/", sync_to_thread=True)
    def index() -> None:
        raise InternalServerErrorHTTPException(template_vars={"reason": "test"})

    @get("/error", sync_to_thread=True)
    def error() -> None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @get("/verbose_error", sync_to_thread=True)
    def verbose_error() -> None:
        raise InternalServerErrorHTTPException(template_vars={"reason": "test"})

    @get("/general_error", sync_to_thread=True)
    def general_error() -> None:
        msg = "My bad!"
        raise ValueError(msg) from None

    app = Litestar(
        [index, error, verbose_error, general_error],
        exception_handlers={
            BaseVerboseHTTPException: verbose_http_exception_handler,
        },
    )
    with TestClient(
        app=app,
        base_url="http://test/",
    ) as c:
        yield c


@pytest.fixture()
def test_app_all_verbose():  # noqa: ANN201

    @get("/", sync_to_thread=True)
    def index(a: Literal[1, 2], b: int) -> dict[str, str]:
        return {"message": f"{a} {b}"}

    @get("/error", sync_to_thread=True)
    def error() -> None:  # type: ignore reportUnusedFunction
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="test detail")

    @get("/verbose_error", sync_to_thread=True)
    def verbose_error() -> None:  # type: ignore reportUnusedFunction
        raise InternalServerErrorHTTPException(template_vars={"reason": "test"})

    @get("/general_error", sync_to_thread=True)
    def general_error() -> None:  # type: ignore reportUnusedFunction
        msg = "My bad!"
        raise ValueError(msg)

    @get("/no_content_error", sync_to_thread=True)
    def no_content_ignored() -> None:  # type: ignore reportUnusedFunction
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    app = Litestar(
        [index, error, verbose_error, general_error, no_content_ignored],
        exception_handlers={
            BaseVerboseHTTPException: verbose_http_exception_handler,
            HTTPException: any_http_exception_handler,
            ValidationException: verbose_request_validation_error_handler,
            Exception: python_error_handler,
        },
    )
    with TestClient(
        app=app,
        base_url="http://test/",
    ) as c:
        yield c


@pytest.fixture()
def attr_rules() -> "ValidationAttrFindType":
    return {
        'query': [r"query parameter \'(.*)\' for"],
    }


@pytest.fixture()
def location_rules() -> "ValidationLocationFindType":
    return {
        'query': [
            "Missing required query parameter",
        ],
        'body': ["number of multipart components exceeds the allowed limit of"],
        'path': [
            'Missing required path parameter',
        ],
        'cookie': [
            'Missing required cookie parameter',
        ],
        'header': [
            'Missing required header parameter',
        ],
    }


@pytest.fixture()
def type_rules() -> "ValidationTypeFindType":
    return {
        'literal_error': {
            'match': 'startswith',
            'pattern': 'Invalid enum value',
        },
        'incorrect_type': {
            'match': 'regex',
            'pattern': r'Expected `.*`, got `.*`',
        },
        'missing': {
            'match': 'startswith',
            'pattern': 'Missing required query parameter',
        },
        'invalid_method': {
            'match': 'startswith',
            'pattern': 'Invalid HTTP method',
        },
        'etag_incorrect_value': {
            'match': 'equals',
            'pattern': 'value must only contain ASCII printable characters',
        },
        'etag_no_value': {
            'match': 'equals',
            'pattern': 'value must be set if documentation_only is false',
        },
        'too_many_multipart_components': {
            'match': 'startswith',
            'pattern': 'number of multipart components exceeds the allowed limit of',
        },
    }
