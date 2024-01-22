"""Typed wrappers for functools.cache and functools.lru_cache decorators."""

import functools
from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def cache(func: Callable[P, R]) -> Callable[P, R]:
    """Preserve function signature and wrap with functools.cache decorator."""
    @functools.wraps(func)
    @functools.cache
    def _wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return func(*args, **kwargs)

    return _wrapper  # type: ignore


def lru_cache(
    func: Callable[P, R], maxsize: int | None = 128, typed: bool = False
) -> Callable[P, R]:
    """Preserve function signature and wrap with functools.lru_cache decorator."""
    @functools.wraps(func)
    @functools.lru_cache(maxsize=maxsize, typed=typed)
    def _wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return func(*args, **kwargs)

    return _wrapper  # type: ignore
