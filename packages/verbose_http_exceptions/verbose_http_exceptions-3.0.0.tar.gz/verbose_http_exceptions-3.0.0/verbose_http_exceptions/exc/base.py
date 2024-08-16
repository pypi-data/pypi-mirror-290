"""Module with base implementation of verbose HTTP exceptions."""

import warnings
from string import Template
from typing import Any, NotRequired, TypedDict

from dev_utils.abstract import Abstract, abstract_class_property
from dev_utils.common import get_object_class_absolute_name

from verbose_http_exceptions.warns import IncorrectExceptionUsageWarning

ABSTRACT_PROPERTY_DEFAULT_VALUE = "<abstract property>"
ABSTRACT_CLS_DEFAULT_VALUE = "<class with abstract properties>"


class VerboseHTTPExceptionDict(TypedDict):
    """TypedDict for verbose http exceptions."""

    code: str
    type: str
    message: str
    location: str | None
    attr: str | None
    nested_errors: NotRequired[list["VerboseHTTPExceptionDict"]]


class BaseVerboseHTTPException(Abstract, Exception):  # noqa: N818
    """Base verbose HTTP-exception.

    Exception has abstract class properties, which must be set in inherited classes.

    Properties description
    ----------------------

    ``status_code``
        HTTP status code (use fastapi.status for it).

    ``code``
        Error code (like "server_error", "validation_error") - general identity.

    ``type_``
        Error code type used as description of code property. For example, if there
        is validation_error in code, you can specify it with "required" type_
        to show, that validation error raises because of required field was not passed
        in request body/query/header/cookie.

    ``message``
        Error message used as description of type_ property. For example, for "required"
        type_ you can specify it with "This field is required" message to show verbose message
        in response.

    Optional class properties
    -------------------------

    There are some optional properties, which could be passed in inherited class to specify some
    extra context.

    ``template``
        Message template, that will be used, if any extra attributes fill be passed in ``as_dict``
        method, or ``from_template`` will be executed directly.

    Dynamic attributes
    ------------------

    Dynamic attributes can be passed only in instances of verbose exceptions.

    ``location``
        Specific location of error. For example, in "validation_error" you can pass location as
        "body" or "query" or "headers" or "queries" or some other location (maybe your custom, if
        you want).

    ``attr``
        Specific attribute name, that cause the error. For example, in "validation_error" your attr
        can be any field, which was used in validation, and which was the reason, why this
        validation error was raised.

    ``nested_errors``
        list of nested BaseVerboseHTTPException information. Necessary for multiple errors in one
        response. For example, in "validation_error" you can pass exceptions about multiple attrs
        were not passed, but required.
    """

    status_code: int = abstract_class_property(int)
    code: str = abstract_class_property(str)
    type_: str = abstract_class_property(str)
    message: str = abstract_class_property(str)

    template: Template | str | None = None

    location: str | None = None
    attr: str | None = None
    nested_errors: list["BaseVerboseHTTPException"] | None = None
    headers: dict[str, str] | None = None

    def __init__(  # noqa: C901, PLR0912, PLR0913
        self,
        *nested_errors: "BaseVerboseHTTPException",
        status_code: int | None = None,
        code: str | None = None,
        type_: str | None = None,
        message: str | None = None,
        location: str | None = None,
        attr_name: str | None = None,
        template_vars: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        if message is not None and template_vars is not None:
            msg = (
                "Template vars and message passed at the same time. "
                "It may cause unexpected behavior."
            )
            warnings.warn(
                msg,
                IncorrectExceptionUsageWarning,
                stacklevel=2,
            )
        if attr_name is not None:
            self.attr = attr_name
        if location is not None:
            self.location = location
        if status_code is not None:
            self.status_code = status_code
        if code is not None:
            self.code = code
        if type_ is not None:
            self.type_ = type_
        if message is not None:
            self.message = message
        if template_vars is not None:
            if isinstance(self.template, Template):
                self.message = self.template.safe_substitute(**template_vars)
            elif isinstance(self.template, str):
                self.message = self.template.format(**template_vars)
            else:
                msg = "Template vars passed but there is no template."
                warnings.warn(msg, IncorrectExceptionUsageWarning, stacklevel=2)
        if nested_errors:
            self.nested_errors = list(nested_errors)
        if headers is not None:
            self.headers = headers

    def _get_attribute_repr(self, name: str) -> Any:  # noqa: ANN401  # pragma: no coverage
        """Safe getattr for verbose http exceptions."""
        try:
            return repr(getattr(self, name))
        except (AttributeError, TypeError):
            return ABSTRACT_PROPERTY_DEFAULT_VALUE

    def __repr__(self) -> str:  # noqa: D105
        cls_path = get_object_class_absolute_name(self.__class__)
        attrs = (
            f'status_code={self.status_code}, code={self._get_attribute_repr("code")}, '
            f'type={self._get_attribute_repr("type_")}, '
            f'message={self._get_attribute_repr("message")}, location={self.location}, '
            f'template={self.template}, attr={self.attr}, headers={self.headers}'
        )
        return f"{cls_path}({attrs})"

    def __str__(self) -> str:  # noqa: D105  # pragma: no coverage
        try:
            return self.message
        except (AttributeError, TypeError):
            return ABSTRACT_CLS_DEFAULT_VALUE

    def as_dict(self) -> VerboseHTTPExceptionDict:
        """Convert Exception instance into dict.

        Usage:
        ```
        class SomeClass(BaseVerboseHTTPException):
            code = 'abc'
            type_ = 'abc'
            message = 'abc'
            template = Template('abc with template : $abc')

        SomeClass(attr_name='my_attr', template_vars={'abc': '25'}).as_dict()
        ```

        Due to this code, returning dict will be the following:

        >>> SomeClass(attr_name='my_attr', template_vars={'abc': '25'}).as_dict()
        {"code": "abc", "type": "abc", "message": "abc with template : 25", "attr": "my_attr"}
        """
        if self.nested_errors is not None:
            return {
                "code": self.code,
                "type": self.type_,
                "message": self.message,
                "location": self.location,
                "attr": self.attr,
                "nested_errors": [nested_error.as_dict() for nested_error in self.nested_errors],
            }
        return {
            "code": self.code,
            "type": self.type_,
            "message": self.message,
            "location": self.location,
            "attr": self.attr,
        }
