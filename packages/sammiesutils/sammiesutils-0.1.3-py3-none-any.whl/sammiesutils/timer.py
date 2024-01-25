"""A simple timer context manager and decorator."""

import time
from collections.abc import Iterator
from contextlib import contextmanager


class Timer:
    """A basic code timer."""

    def __init__(self) -> None:
        """Create a timer."""
        self.start_time = time.perf_counter()
        self.end_time: float | None = None

    @property
    def elapsed(self) -> float:
        """Seconds elapsed since timer creation."""
        return time.perf_counter() - self.start_time


@contextmanager
def timer(print_elapsed: bool = False) -> Iterator[Timer]:
    """
    Time the indented block.
    Yields a Timer object with `elapsed` and `end_time` properties.
    """
    timer = Timer()
    yield timer
    timer.end_time = timer.elapsed
    if print_elapsed:
        print(f"{timer.end_time:.8f} seconds elapsed.")
