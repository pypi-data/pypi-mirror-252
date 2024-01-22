"""A simple timer context manager and decorator."""

import functools
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


@contextmanager
def timer(decimal_places: int = 5) -> Iterator[None]:
    """Time the indented block and print time elapsed."""
    start_time = time.perf_counter()
    yield None
    elapsed = time.perf_counter() - start_time
    print(f"{elapsed:.{decimal_places}f} seconds elapsed.")


def timed(decimal_places: int = 5) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Print seconds elapsed in decorated function after call."""

    def _timed(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def _wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start_time
            print(f"{elapsed:.{decimal_places}f} seconds elapsed.")
            return result

        return _wrapper

    return _timed
