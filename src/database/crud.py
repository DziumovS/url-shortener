from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import ShortURL
from src.exceptions import SlugAlreadyExistsError


async def add_slug_to_db(
    slug: str,
    original_url: str,
    session: AsyncSession,
):
    new_slug = ShortURL(
        slug=slug,
        original_url=original_url
    )
    session.add(new_slug)
    try:
        await session.commit()
    except IntegrityError:
        raise SlugAlreadyExistsError


async def get_original_url_from_db(
    slug: str,
    session: AsyncSession
) -> str | None:
    query = select(ShortURL).filter_by(slug=slug)
    response = await session.execute(query)
    result: ShortURL | None = response.scalar_one_or_none()

    return result.original_url if result.original_url else None
