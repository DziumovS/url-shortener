from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import ShortURL


async def add_slug_to_db(
    slug: str,
    original_url: str,
    session: AsyncSession,
) -> str:
    stmt = (
        insert(ShortURL)
        .values(slug=slug, original_url=original_url)
        .on_conflict_do_nothing(index_elements=["original_url"])
        .returning(ShortURL.slug)
    )

    result = await session.execute(stmt)
    created_slug = result.scalar_one_or_none()

    if created_slug:
        await session.commit()
        return created_slug

    query = select(ShortURL.slug).where(ShortURL.original_url == original_url)
    result = await session.execute(query)

    return result.scalar_one()


async def get_original_url_from_db(
    slug: str,
    session: AsyncSession
) -> str | None:
    query = select(ShortURL).filter_by(slug=slug)
    response = await session.execute(query)
    result: ShortURL | None = response.scalar_one_or_none()

    if result is None:
        return None

    return result.original_url
