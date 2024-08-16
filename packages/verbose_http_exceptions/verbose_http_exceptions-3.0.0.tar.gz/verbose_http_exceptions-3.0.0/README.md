
# Verbose HTTP exceptions

[![PyPI version](https://badge.fury.io/py/verbose-http-exceptions.svg)](https://badge.fury.io/py/verbose_http_exceptions)
![coverage](./coverage.svg)

[![types - Mypy](https://img.shields.io/badge/types-Pyright-2ecf29.svg?logo=python&color=3ec965&logoColor=ffffff&labelColor=353b42)](https://github.com/python/mypy)
[![License - MIT](https://img.shields.io/badge/license-MIT-2ecf29.svg?logo=python&color=3ec965&logoColor=ffffff&labelColor=353b42)](https://spdx.org/licenses/)
[![code style](https://img.shields.io/badge/code_style-Ruff-2ecf29.svg?logo=python&color=3ec965&logoColor=ffffff&labelColor=353b42)](https://github.com/astral-sh/ruff)
[![CI actions status](https://github.com/ALittleMoron/verbose_http_exceptions/actions/workflows/ci.yaml/badge.svg)](https://github.com/ALittleMoron/verbose_http_exceptions/actions)
[![Release actions status](https://github.com/ALittleMoron/verbose_http_exceptions/actions/workflows/release.yaml/badge.svg)](https://github.com/ALittleMoron/verbose_http_exceptions/actions)

## For what?

I made this package to make my work with http exceptions more easier. In FastAPI I had problem
with HTTP exceptions - they are too simple. Only `detail` field and that is all. And other tools
that make http exceptions more verbose works not like I expect.

This package was inspired by [drf-exceptions-hog](https://github.com/PostHog/drf-exceptions-hog),
but implemented for other Web-frameworks.

## Install

To install the package you need you run the following commands.

For pip:

```bash
pip install verbose_http_exceptions
```

For poetry:

```bash
poetry add verbose_http_exceptions
```

For PDM:

```bash
pdm add verbose_http_exceptions
```

## Usage

You can use all these exceptions for your need even without any web-framework, but mostly, it may
be useless, so use extensions in this package or write your own, if you need.

Then all (or some specific part of) your exceptions will be returned to users in JSON like this:

```json
{
    "code": "validation_error",
    "type": "literal_error",
    "message": "Input should be 1 or 2",
    "attr": "a",
    "location": "query",
}
```

or this (multiple exceptions supported too):

```json
{
    "code": "multiple",
    "type": "multiple",
    "message": "Multiple exceptions ocurred. Please check list for details.",
    "attr": null,
    "location": null,
    "nested_errors": [
        {
            "code": "validation_error",
            "type": "literal_error",
            "message": "Input should be 1 or 2",
            "attr": "a",
            "location": "query",
        },
        {
            "code": "validation_error",
            "type": "missing",
            "message": "Field required",
            "attr": "b",
            "location": "query",
        }
    ]
}
```

### FastAPI implementation

To work with this utility you must add exception handlers in your FastAPI project like this:

```python
from fastapi import FastAPI
from verbose_http_exceptions.ext.fastapi import (
    apply_verbose_http_exception_handler,
    apply_all_handlers,
)

app = FastAPI()
apply_all_handlers(app)
# or
apply_verbose_http_exception_handler(app)
# See document-strings of functions for more information.
```

> [!NOTE] Specific use
> Package contains appliers, which add handlers to FastAPI instance, and handlers itself, so
> you can work with them directly. Import them from regular package path or pass `.handlers` to it.

> [!TIP]
> `apply_all_handler` function also has `override_422_openapi` param (default True). You can turn
> it off to avoid overriding 422 errors in your application OpenAPI schema.

### Litestar implementation

To work with this utility you must add exception handlers in your Litestar project like this:

```python
from litestar import Litestar
from verbose_http_exceptions.ext.litestar import ALL_EXCEPTION_HANDLERS_MAP

app = Litestar(
    exception_handlers=ALL_EXCEPTION_HANDLERS_MAP
)
```

> [!NOTE] Specific use
> `ALL_EXCEPTION_HANDLERS_MAP` is a ready to use dictionary with all exception handlers. Extension
> has other handlers and handler mappings, so you can import them directly with Litestar instance.

> [!WARNING] Possible incorrect use
> Make sure, you pass handlers and handler mappings correctly, because they are not general,
> so algorithms inside them can be different, and if you pass, for example, `python_error_handler`
> with litestar `ValidationException`, server will always return 500 internal server error without
> any context, if there is validation request error raised.

## What is next?

I like this project, and I want to implement it for many web-frameworks and add new functionality,
so my goals are to:

- [x] Integrate this package with [litestar](https://github.com/litestar-org/litestar).
- [ ] Add OpenAPI override for Litestar.
  FastAPI already has override functionality to add to 422 errors verbose schema and description.
- [x] Add all http-exceptions for all status codes.
- [x] Add status codes module to make work with my package easier.
- [ ] Add tests for all exceptions (Now only specific errors tested for coverage).
- [ ] Add extra mapping to response (Litestar compatibility + good idea itself), but pass
  only important context.
- [ ] Add other content response types like XML.
