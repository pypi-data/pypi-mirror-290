from typing import TYPE_CHECKING, Any, Literal, TypeAlias, TypedDict

if TYPE_CHECKING:
    from collections.abc import Callable, MutableMapping
    from re import Pattern

    from litestar import Request, Response


class TypeSearchSetting(TypedDict):
    """Dict with rules for searching for some string contains."""

    match: Literal["regex", "startswith", 'equals']
    pattern: str


ValidationAttrFindType: TypeAlias = dict[str, list["str | Pattern[str]"]]
ValidationLocationFindType: TypeAlias = dict[str, list["str | Pattern[str]"]]
ValidationTypeFindType: TypeAlias = dict[str, TypeSearchSetting]
LitestarExceptionHandler: TypeAlias = "Callable[[Request[Any, Any, Any], Exception], Response[Any]]"
LitestarExceptionHandlersMap: TypeAlias = (
    "MutableMapping[int | type[Exception], LitestarExceptionHandler]"
)
