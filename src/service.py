from sqlalchemy.ext.asyncio import AsyncSession

from src.database.crud import add_slug_to_db, get_original_url_from_db
from src.exceptions import NoOriginalUrlFoundError, SlugAlreadyExistsError
from src.shortener import generate_random_slug
from src.decorators import retry


@retry(10, (SlugAlreadyExistsError,))
async def generate_short_url(
    original_url: str,
    session: AsyncSession
) -> str:
    slug = generate_random_slug()
    await add_slug_to_db(slug, original_url, session)

    return slug


async def get_url_by_slug(
    slug: str,
    session: AsyncSession
) -> str:
    original_url = await get_original_url_from_db(slug, session)
    if not original_url:
        raise NoOriginalUrlFoundError()

    return original_url
