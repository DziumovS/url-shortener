import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.crud import add_slug_to_db, get_original_url_from_db
from src.utils.shortener import generate_random_slug


@pytest.mark.asyncio
async def test_add_and_get_slug(session: AsyncSession) -> None:
    url = "https://my-site.com"
    slug = "abc123"

    created_slug = await add_slug_to_db(slug, url, session)

    result = await get_original_url_from_db(created_slug, session)
    assert result == url


@pytest.mark.asyncio
async def test_get_missing_slug(session: AsyncSession) -> None:
    result = await get_original_url_from_db("missing", session)
    assert result is None


@pytest.mark.asyncio
async def test_add_slug_idempotent(session: AsyncSession) -> None:
    url = "https://my-site.com"

    slug1 = generate_random_slug()
    slug2 = await add_slug_to_db(slug1, url, session)

    slug3 = await add_slug_to_db(generate_random_slug(), url, session)

    assert slug3 == slug2
