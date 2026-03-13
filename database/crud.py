from sqlalchemy import select

from database.database import new_session
from database.models import ShortURL


async def add_slug_to_db(
    slug: str,
    original_url: str,
):
    async with new_session() as session:
        new_slug = ShortURL(
            slug=slug,
            original_url=original_url
        )
        session.add(new_slug)
        await session.commit()


async def get_original_url_from_db(slug: str) -> str | None:
    async with new_session() as session:
        query = select(ShortURL).filter_by(slug=slug)
        response = await session.execute(query)
        result: ShortURL | None = response.scalar_one_or_none()

        return result.original_url if result.original_url else None
