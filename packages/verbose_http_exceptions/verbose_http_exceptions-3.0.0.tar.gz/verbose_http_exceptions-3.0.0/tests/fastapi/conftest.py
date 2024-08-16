from typing import Literal

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from verbose_http_exceptions.exc import InternalServerErrorHTTPException
from verbose_http_exceptions.ext.fastapi import (
    apply_all_handlers,
    apply_verbose_http_exception_handler,
)
from verbose_http_exceptions.ext.fastapi.appliers import apply_python_errors_handling_middleware


@pytest.fixture()
def test_app_only_verbose():  # noqa: ANN201
    app = FastAPI()

    @app.get("/")
    def index():  # type: ignore reportUnusedFunction # noqa: ANN202
        raise InternalServerErrorHTTPException(template_vars={"reason": "test"})

    @app.get("/error")
    def error():  # type: ignore reportUnusedFunction # noqa: ANN202
        raise HTTPException(status_code=500, detail="test detail")

    @app.get("/verbose_error")
    def verbose_error():  # type: ignore reportUnusedFunction # noqa: ANN202
        raise InternalServerErrorHTTPException(template_vars={"reason": "test"})

    @app.get("/general_error")
    def general_error():  # type: ignore reportUnusedFunction # noqa: ANN202
        msg = "My bad!"
        raise ValueError(msg) from None

    apply_verbose_http_exception_handler(app)

    with TestClient(
        app=app,
        base_url="http://test/",
    ) as c:
        yield c


@pytest.fixture()
def test_app_all_verbose():  # noqa: ANN201
    app = FastAPI()

    @app.get("/")
    def index(a: Literal["1", "2"], b: Literal["25"]):  # type: ignore reportUnusedFunction  # noqa: ANN202, ARG001
        return {"message": "abc"}

    @app.get("/error")
    def error():  # type: ignore reportUnusedFunction # noqa: ANN202
        raise HTTPException(status_code=500, detail="test detail")

    @app.get("/verbose_error")
    def verbose_error():  # type: ignore reportUnusedFunction # noqa: ANN202
        raise InternalServerErrorHTTPException(template_vars={"reason": "test"})

    @app.get("/general_error")
    def general_error():  # type: ignore reportUnusedFunction # noqa: ANN202
        msg = "My bad!"
        raise ValueError(msg)

    @app.get("/no_content_error")
    def no_content_ignored():  # type: ignore reportUnusedFunction # noqa: ANN202
        raise HTTPException(status_code=204)

    apply_all_handlers(app)
    apply_python_errors_handling_middleware(app)
    with TestClient(
        app=app,
        base_url="http://test/",
    ) as c:
        yield c
