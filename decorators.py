import functools


def retry(attempts: int, exceptions: tuple[type[Exception], ...]):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_exc = None

            for attempt in range(attempts):
                try:
                    return await func(*args, **kwargs)

                except exceptions as ex:
                    last_exc = ex

                    if attempt == attempts - 1:
                        raise

            raise last_exc

        return wrapper

    return decorator
