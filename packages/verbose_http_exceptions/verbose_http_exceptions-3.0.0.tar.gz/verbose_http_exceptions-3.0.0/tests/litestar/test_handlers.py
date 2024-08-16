from typing import TYPE_CHECKING

from litestar import status_codes as status

if TYPE_CHECKING:
    from litestar import Litestar
    from litestar.testing import TestClient


base_500_result = {
    "code": "server_error",
    "type": "internal_server_error",
    "attr": None,
    "location": None,
}
expected_error_500_result = {
    **base_500_result,
    "message": "Internal server error was found: test.",
}
expected_http_exception_500_result = {
    **base_500_result,
    "message": "test detail",
}


def test_all_verbose_handlers_400(test_app_all_verbose: "TestClient[Litestar]") -> None:
    response = test_app_all_verbose.get("/?a=25&b=abc")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "code": "multiple",
        "type": "multiple",
        "message": "Multiple errors ocurred. Please check list for nested_errors.",
        "attr": None,
        "location": None,
        "nested_errors": [
            {
                "code": "validation_error",
                "type": "literal_error",
                "message": "Invalid enum value 25",
                "attr": "a",
                "location": "query",
            },
            {
                "code": "validation_error",
                "type": "incorrect_type",
                "message": r"Expected `int`, got `str`",
                "attr": "b",
                "location": "query",
            },
        ],
    }


def test_all_verbose_handlers_400_one_error(test_app_all_verbose: "TestClient[Litestar]") -> None:
    response = test_app_all_verbose.get("/?a=1")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "code": "validation_error",
        "type": "missing",
        "message": "Missing required query parameter 'b' for path /?a=1",
        "attr": 'b',
        "location": "query",
    }


def test_all_verbose_handlers_http(test_app_all_verbose: "TestClient[Litestar]") -> None:
    response = test_app_all_verbose.get("/error")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == expected_http_exception_500_result


def test_all_verbose_handlers_http_verbose(test_app_all_verbose: "TestClient[Litestar]") -> None:
    response = test_app_all_verbose.get("/verbose_error")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == expected_error_500_result


def test_all_verbose_handlers_skip_204_error(test_app_all_verbose: "TestClient[Litestar]") -> None:
    response = test_app_all_verbose.get("/no_content_error")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not response.content


def test_all_verbose_handlers_non_http(test_app_all_verbose: "TestClient[Litestar]") -> None:
    response = test_app_all_verbose.get("/general_error")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {
        **base_500_result,
        "message": "My bad!",
    }


def test_only_verbose_handlers(test_app_only_verbose: "TestClient[Litestar]") -> None:
    response = test_app_only_verbose.get("/")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == expected_error_500_result


def test_only_verbose_handlers_with_litestar_http_exception(
    test_app_only_verbose: "TestClient[Litestar]",
) -> None:
    response = test_app_only_verbose.get("/error")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"status_code": 500, "detail": "Internal Server Error"}
