import functools
from collections.abc import Awaitable, Callable
from typing import TypeVar, ParamSpec


P = ParamSpec("P")
R = TypeVar("R")


def retry(
    attempts: int,
    exceptions: tuple[type[Exception], ...],
) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for attempt in range(attempts):
                try:
                    return await func(*args, **kwargs)
                except exceptions:
                    if attempt == attempts - 1:
                        raise

            raise RuntimeError("Retry failed unexpectedly")

        return wrapper

    return decorator
