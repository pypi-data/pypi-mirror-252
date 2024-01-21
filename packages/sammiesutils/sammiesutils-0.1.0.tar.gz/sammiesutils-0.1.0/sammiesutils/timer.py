"""A simple timer context manager."""

import time
from collections.abc import Iterator
from contextlib import contextmanager


@contextmanager
def timer(decimal_places: int = 5) -> Iterator[None]:
    """Time the indented block and print time elapsed."""
    start_time = time.perf_counter()
    yield None
    elapsed = time.perf_counter() - start_time
    print(f"{round(elapsed, decimal_places)} seconds elapsed.")
