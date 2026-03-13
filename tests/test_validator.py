import pytest
from pydantic import ValidationError

from src.schemas.url import URLInput


@pytest.mark.parametrize(
    "url",
    [
        "https://google.com",
        "http://example.org",
        "https://sub.domain.com/path",
        "ftp://ftp.example.com/file.txt",
        "tg://resolve?domain=telegram",
        "mailto:test@example.com",
        "whatsapp://send?phone=123456789",
    ],
)
def test_valid_urls(url):
    data = URLInput(original_url=url)
    assert data.original_url == url


@pytest.mark.parametrize(
    "url",
    [
        "javascript:alert(1)",
        "https://google.com@evil.com",
        "http://localhost",
        "http://127.0.0.1",
        "https://invalid-domain",
        "not-a-url",
        "",
    ],
)
def test_invalid_urls(url):
    with pytest.raises(ValidationError):
        URLInput(original_url=url)


def test_too_long_url():
    url = "https://example.com/" + "a" * 5000

    with pytest.raises(ValidationError):
        URLInput(original_url=url)
