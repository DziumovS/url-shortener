from httpx import AsyncClient


async def test_generate_slug(ac: AsyncClient):
    result = await ac.post("/short_url", json={"original_url": "https://my-site.com"})
