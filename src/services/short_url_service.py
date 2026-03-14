from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.crud import add_slug_to_db, get_original_url_from_db
from src.decorators.decorators import retry
from src.utils.shortener import generate_random_slug
from src.exceptions.exceptions import SlugAlreadyExistsError, NoOriginalUrlFoundError
from src.db.redis_cache import cache_slug, get_cached_url


@retry(10, (SlugAlreadyExistsError,))
async def generate_short_url(original_url: str, session: AsyncSession) -> str:
    slug = generate_random_slug()

    try:
        created_slug = await add_slug_to_db(slug, original_url, session)
        await cache_slug(created_slug, original_url)

        return created_slug

    except IntegrityError:
        raise SlugAlreadyExistsError()


async def get_url_by_slug(slug: str, session: AsyncSession) -> str:
    cached = await get_cached_url(slug)

    if cached:
        return cached

    original_url = await get_original_url_from_db(slug, session)

    if not original_url:
        raise NoOriginalUrlFoundError()

    await cache_slug(slug, original_url)

    return original_url
