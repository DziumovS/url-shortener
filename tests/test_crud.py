import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.crud import add_slug_to_db, get_original_url_from_db
from src.exceptions import SlugAlreadyExistsError


@pytest.mark.asyncio
async def test_add_and_get_slug(session: AsyncSession) -> None:
    slug = "abc123"
    url = "https://my-site.com"

    await add_slug_to_db(slug, url, session)

    result = await get_original_url_from_db(slug, session)

    assert result == url


@pytest.mark.asyncio
async def test_get_missing_slug(session: AsyncSession) -> None:
    result = await get_original_url_from_db("missing", session)

    assert result is None


@pytest.mark.asyncio
async def test_slug_unique_constraint(session: AsyncSession) -> None:
    slug = "same123"
    url = "https://my-site.com"

    await add_slug_to_db(slug, url, session)

    with pytest.raises(SlugAlreadyExistsError):
        await add_slug_to_db(slug, url, session)
