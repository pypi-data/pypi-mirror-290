from typing import TYPE_CHECKING

from verbose_http_exceptions import status

if TYPE_CHECKING:
    from verbose_http_exceptions.ext.litestar.types import (
        ValidationAttrFindType,
        ValidationLocationFindType,
        ValidationTypeFindType,
    )

NO_CONTENT_STATUS_CODES = {
    status.HTTP_100_CONTINUE,
    status.HTTP_101_SWITCHING_PROTOCOLS,
    status.HTTP_102_PROCESSING,
    status.HTTP_103_EARLY_HINTS,
    status.HTTP_204_NO_CONTENT,
    status.HTTP_304_NOT_MODIFIED,
}
"""Set of status codes, which must be without any content.

See litestar documentation: https://docs.litestar.dev/2/usage/responses.html#status-codes
"""

VALIDATION_TYPE_MAPPING: "ValidationTypeFindType" = {
    'literal_error': {
        'match': 'startswith',
        'pattern': 'Invalid enum value',
    },
    'incorrect_type': {
        'match': 'regex',
        'pattern': r'Expected `.*`, got `.*`',
    },
    'missing': {
        'match': 'regex',
        'pattern': r'Missing required .*? parameter',
    },
    'missing_field': {
        'match': 'equals',
        'pattern': 'Field required',
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
    'less_or_equals_number_violation': {
        'match': 'startswith',
        'pattern': 'Input should be less than or equal to',
    },
    'less_number_violation': {
        'match': 'regex',
        'pattern': r'Input should be less than \d+',
    },
    'greater_or_equals_number_violation': {
        'match': 'startswith',
        'pattern': 'Input should be greater than or equal to',
    },
    'greater_number_violation': {
        'match': 'regex',
        'pattern': r'Input should be greater than \d+',
    },
    'max_length_violation': {
        'match': 'regex',
        'pattern': r'String should have at most \d+ character',
    },
    'min_length_violation': {
        'match': 'regex',
        'pattern': r'String should have at least \d+ character',
    },
    'number_equals_violation': {
        'match': 'regex',
        'pattern': r'Input should be \d+',
    },
    'pattern_mismatch': {
        'match': 'startswith',
        'pattern': 'String should match pattern',
    },
    'not_valid_value_type': {
        'match': 'startswith',
        'pattern': 'Input should be a valid ',
    },
    'user_custom_value_error': {
        'match': 'startswith',
        'pattern': 'Value error, ',
    },
    'user_custom_assertion_error': {
        'match': 'startswith',
        'pattern': 'Assertion failed, ',
    },
}

VALIDATION_ATTR_MAPPING: "ValidationAttrFindType" = {
    'query': [r"query parameter \'(.*)\' for"],
}
VALIDATION_LOCATION_MAPPING: "ValidationLocationFindType" = {
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
