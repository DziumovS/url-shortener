from src.service import generate_short_url


async def test_generate_short_url(session):
    result = await generate_short_url("https://my-site.com", session)
    assert type(result) is str
    assert len(result) == 6
