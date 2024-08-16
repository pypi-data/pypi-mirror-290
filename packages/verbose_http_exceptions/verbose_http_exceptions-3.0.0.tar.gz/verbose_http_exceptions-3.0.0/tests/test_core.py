from string import Template

import pytest

from verbose_http_exceptions import exc as base_http_exceptions
from verbose_http_exceptions.warns import IncorrectExceptionUsageWarning

attr = "attr"
loc = "loc"
code = "test"
test_http_exception1_dict = {
    "code": "test",
    "type": "Test",
    "message": "test message: test",
    "attr": "attr",
    "location": "loc",
}
http_exception_dict_with_nested_errors = {
    "code": "test",
    "type": "Test",
    "message": "test message: test",
    "attr": "attr",
    "location": "loc",
    "nested_errors": [
        {
            "code": "test",
            "type": "Test",
            "message": "test message: test",
            "attr": "attr",
            "location": "loc",
        },
        {
            "code": "test",
            "type": "Test",
            "message": "test message: test",
            "attr": "attr",
            "location": "loc",
        },
    ],
}


class TestHttpException0(base_http_exceptions.BaseVerboseHTTPException):  # noqa: D101
    __test__ = False

    status_code = 400
    code = "test"
    type_ = "Test"
    message = "test message"


class TestHttpException1(base_http_exceptions.BaseVerboseHTTPException):  # noqa: D101
    __test__ = False

    status_code = 400
    code = "test"
    type_ = "Test"
    message = "test message"
    template = Template("test message: $test")


class TestHttpException2(base_http_exceptions.BaseVerboseHTTPException):  # noqa: D101
    __test__ = False

    status_code = 400
    code = "test"
    type_ = "Test"
    message = "test message"
    template = "test message: {test}"


def test_warn_init_with_exist_message_and_template_vars() -> None:
    with pytest.warns(
        IncorrectExceptionUsageWarning,
        match=(
            "Template vars and message passed at the same time. "
            "It may cause unexpected behavior."
        ),
    ):
        TestHttpException2(message='abc', template_vars={"test": "test"})


def test_warn_init_with_template_vars_and_without_template() -> None:
    with pytest.warns(
        IncorrectExceptionUsageWarning,
        match="Template vars passed but there is no template.",
    ):
        TestHttpException0(template_vars={"test": "test"})


def test_class_as_dict_with_init() -> None:
    with pytest.raises(TestHttpException1) as exc_info:
        raise TestHttpException1(
            TestHttpException1(attr_name=attr, location=loc, template_vars={"test": "test"}),
            TestHttpException2(attr_name=attr, location=loc, template_vars={"test": "test"}),
            status_code=1000,
            headers={"X-USER-ID": "25"},
            attr_name=attr,
            location=loc,
            code=code,
            template_vars={"test": "test"},
        )
    assert exc_info.value.status_code == 1000  # noqa: PLR2004
    assert exc_info.value.headers == {"X-USER-ID": "25"}
    assert exc_info.value.as_dict() == http_exception_dict_with_nested_errors


def test_class_repr() -> None:
    with pytest.raises(TestHttpException1) as exc_info:
        raise TestHttpException1
    exc = exc_info.value
    assert repr(exc).startswith(
        (
            "tests.test_core.TestHttpException1(status_code=400, code='test', "
            "type='Test', message='test message', location=None"
        ),
    )
    assert "<string.Template object at " in repr(exc)
    assert repr(exc).endswith("attr=None, headers=None)")


def test_class_str() -> None:
    with pytest.raises(TestHttpException1) as exc_info:
        raise TestHttpException1
    assert str(exc_info.value) == exc_info.value.message
