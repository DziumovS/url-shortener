import functools


def retry(attempts: int, exceptions: tuple[type[Exception], ...]):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(attempts):
                try:
                    return await func(*args, **kwargs)

                except exceptions:
                    if attempt == attempts - 1:
                        raise

        return wrapper

    return decorator
