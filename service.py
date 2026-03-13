from database.crud import add_slug_to_db, get_original_url_from_db
from exceptions import NoOriginalUrlFoundError
from shortener import generate_random_slug


async def generate_short_url(
        original_url: str
) -> str:
    slug = generate_random_slug()
    await add_slug_to_db(slug, original_url)

    return slug


async def get_url_by_slug(slug: str) -> str:
    original_url = await get_original_url_from_db(slug)
    if not original_url:
        raise NoOriginalUrlFoundError()

    return original_url
