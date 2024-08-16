from typing import TYPE_CHECKING

import pytest
from litestar.enums import ParamType

from verbose_http_exceptions.ext.litestar import utils as litestar_utils

if TYPE_CHECKING:
    from verbose_http_exceptions.ext.litestar.types import (
        ValidationAttrFindType,
        ValidationLocationFindType,
        ValidationTypeFindType,
    )


@pytest.mark.parametrize(
    ('message', 'expected_result'),
    [
        (
            'Missing required query parameter \'b\' for path /?a=1',
            'query',
        ),
        (
            'not valid string',
            None,
        ),
    ],
)
def test_find_validation_location(
    message: str,
    expected_result: str | None,
    # fixtures
    location_rules: "ValidationLocationFindType",
) -> None:
    assert (
        litestar_utils.find_validation_location(message=message, rules=location_rules)
        == expected_result
    )


@pytest.mark.parametrize(
    ('message', 'location', 'expected_result'),
    [
        (
            'Missing required query parameter \'b\' for path /?a=1',
            'query',
            'b',
        ),
        (
            'Missing required query parameter \'some2521\' for path /?a=1',
            'query',
            'some2521',
        ),
        (
            'Missing required query parameter \'long_variable_in_snake_case\' for path /?a=1',
            'query',
            'long_variable_in_snake_case',
        ),
        (
            'Missing required query parameter \'c\' for path /?a=1',
            ParamType.QUERY,
            'c',
        ),
        (
            'Missing required query parameter \'b\' for path /?a=1',
            None,
            None,
        ),
        (
            'Missing required query parameter \'b\' for path /?a=1',
            'not_rule',
            None,
        ),
        ('not valid string', 'query', None),
    ],
)
def test_find_validation_attr(
    message: str,
    location: ParamType | str | None,
    expected_result: str | None,
    # fixtures
    attr_rules: "ValidationAttrFindType",
) -> None:
    assert (
        litestar_utils.find_validation_attr(message=message, location=location, rules=attr_rules)
        == expected_result
    )


@pytest.mark.parametrize(
    ('message', 'expected_result'),
    [
        (
            'value must be set if documentation_only is false',
            'etag_no_value',
        ),
        (
            'Missing required query parameter \'b\' for /?a=25',
            'missing',
        ),
        (
            'Expected `int`, got `str`',
            'incorrect_type',
        ),
        (
            'Invalid enum value 25 for query parameter \'b\'',
            'literal_error',
        ),
        (
            'Not known message without any context.',
            None,
        ),
    ],
)
def test_find_validation_type(
    message: str,
    expected_result: str | None,
    # fixtures
    type_rules: "ValidationTypeFindType",
) -> None:
    assert litestar_utils.find_validation_type(message=message, rules=type_rules) == expected_result
