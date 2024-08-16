import re
from typing import Any

from litestar.enums import ParamType

from verbose_http_exceptions.ext.litestar.constants import (
    VALIDATION_ATTR_MAPPING,
    VALIDATION_LOCATION_MAPPING,
    VALIDATION_TYPE_MAPPING,
)
from verbose_http_exceptions.ext.litestar.exc import ValidationHTTPException
from verbose_http_exceptions.ext.litestar.types import (
    ValidationAttrFindType,
    ValidationLocationFindType,
    ValidationTypeFindType,
)


def find_validation_location(
    message: str,
    *,
    rules: ValidationLocationFindType = VALIDATION_LOCATION_MAPPING,
) -> str | None:
    """Find location of error from response message."""
    # TODO(Dmitriy Lunev): refactoring. remove O(N^2).  # noqa: FIX002, TD003
    for location, patterns in rules.items():
        for pattern in patterns:
            finds = re.search(pattern, message)
            if finds:
                return location
    return None


def find_validation_attr(
    message: str,
    location: ParamType | str | None,
    *,
    rules: ValidationAttrFindType = VALIDATION_ATTR_MAPPING,
) -> str | None:
    """Find attribute of error from response message."""
    if isinstance(location, ParamType):
        location = location.value
    if not isinstance(location, str) or location not in rules:
        return None
    patterns = rules[location]
    for pattern in patterns:
        finds = re.search(pattern, message)
        if finds:
            return finds.group(1)
    return None


def find_validation_type(
    message: str,
    *,
    rules: ValidationTypeFindType = VALIDATION_TYPE_MAPPING,
) -> str | None:
    """Return validation error type depends on rules of messages."""
    for type_, search_settings in rules.items():
        match search_settings['match']:
            case 'regex':
                is_matched = bool(re.match(search_settings['pattern'], message))
            case 'startswith':
                is_matched = message.startswith(search_settings['pattern'])
            case 'equals':
                is_matched = message == search_settings['pattern']
            case _:  # type: ignore[reportUnnecessaryComparison]  # pragma: no cover
                return None
        if is_matched:
            return type_
    return None


def validation_error_from_error_dict(
    error: dict[str, Any],
    *,
    location_rules: ValidationLocationFindType = VALIDATION_LOCATION_MAPPING,
    type_rules: ValidationTypeFindType = VALIDATION_TYPE_MAPPING,
    attr_rules: ValidationAttrFindType = VALIDATION_ATTR_MAPPING,
) -> ValidationHTTPException:
    """Convert error dict to ValidationHTTPException instance."""
    message = error.get("message") or "__not_known_message__"
    raw_location = error.get("source")
    location = (
        raw_location.value if isinstance(raw_location, ParamType) else raw_location
    ) or find_validation_location(message=message, rules=location_rules)
    attr_name = error.get("key") or find_validation_attr(
        message=message,
        location=location,
        rules=attr_rules,
    )
    type_ = (
        error.get("type")
        or find_validation_type(
            message=message,
            rules=type_rules,
        )
        or "__not_known_type__"
    )
    return ValidationHTTPException(
        type_=type_,
        message=message,
        location=location,
        attr_name=attr_name,
    )
