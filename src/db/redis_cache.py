from src.db.redis_client import redis_client
from src.config import config as c


def _key(slug: str) -> str:
    return f"shorturl:{slug}"


async def cache_slug(slug: str, original_url: str) -> None:
    await redis_client.set(
        _key(slug),
        original_url,
        ex=c.REDIS_TTL_SECONDS,
    )


async def get_cached_url(slug: str) -> str | None:
    key = _key(slug)

    url = await redis_client.get(key)

    if url:
        await redis_client.expire(key, c.REDIS_TTL_SECONDS)

    return url
