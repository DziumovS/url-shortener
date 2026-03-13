import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_generate_slug_api(ac: AsyncClient) -> None:
    response = await ac.post(
        "/c",
        json={"original_url": "https://my-site.com"},
    )

    assert response.status_code == 200

    data = response.json()

    assert "data" in data
    assert len(data["data"]) == 6


@pytest.mark.asyncio
async def test_redirect_api(ac: AsyncClient) -> None:
    create = await ac.post(
        "/c",
        json={"original_url": "https://my-site.com"},
    )

    assert create.status_code == 200

    slug = create.json()["data"]

    response = await ac.get(f"/g/{slug}", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["location"] == "https://my-site.com"


@pytest.mark.asyncio
async def test_redirect_missing_slug(ac: AsyncClient) -> None:
    response = await ac.get("/missing")

    assert response.status_code == 404
