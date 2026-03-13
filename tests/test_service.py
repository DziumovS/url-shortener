import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.short_url_service import generate_short_url, get_url_by_slug
from src.exceptions import NoOriginalUrlFoundError


@pytest.mark.asyncio
async def test_generate_short_url(session: AsyncSession) -> None:
    slug = await generate_short_url("https://my-site.com", session)

    assert isinstance(slug, str)
    assert len(slug) == 6


@pytest.mark.asyncio
async def test_get_url_by_slug(session: AsyncSession) -> None:
    slug = await generate_short_url("https://my-site.com", session)

    url = await get_url_by_slug(slug, session)

    assert url == "https://my-site.com"


@pytest.mark.asyncio
async def test_get_url_by_missing_slug(session: AsyncSession) -> None:
    with pytest.raises(NoOriginalUrlFoundError):
        await get_url_by_slug("missing", session)
