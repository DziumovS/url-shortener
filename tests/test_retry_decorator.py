import pytest

from src.decorators.decorators import retry


class RetryTestError(Exception):
    pass


@pytest.mark.asyncio
async def test_retry_success() -> None:
    counter = {"count": 0}

    @retry(3, (RetryTestError,))
    async def fn() -> int:
        counter["count"] += 1
        if counter["count"] < 2:
            raise RetryTestError()
        return 1

    result = await fn()

    assert result == 1
    assert counter["count"] == 2


@pytest.mark.asyncio
async def test_retry_failure() -> None:
    @retry(2, (RetryTestError,))
    async def fn() -> None:
        raise RetryTestError()

    with pytest.raises(RetryTestError):
        await fn()
