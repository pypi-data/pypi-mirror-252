"""Typed cache decorator."""

import functools
from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def cache(func: Callable[P, R]) -> Callable[P, R]:
    """Decorate a function with @functools.cache without losing its signature."""

    @functools.wraps(func)
    @functools.cache
    def _wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return func(*args, **kwargs)

    return _wrapper  # type: ignore
