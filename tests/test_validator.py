import pytest
from pydantic import ValidationError

from src.schemas.url import URLInput


def test_valid_http_url():
    data = URLInput(original_url="https://google.com")
    assert data.original_url == "https://google.com"


def test_valid_ftp_url():
    data = URLInput(original_url="ftp://ftp.example.com/file.txt")
    assert data.original_url.startswith("ftp://")


def test_valid_messenger_url():
    data = URLInput(original_url="tg://resolve?domain=telegram")
    assert data.original_url.startswith("tg://")


def test_invalid_url():
    with pytest.raises(ValidationError):
        URLInput(original_url="not-a-url")


def test_invalid_domain():
    with pytest.raises(ValidationError):
        URLInput(original_url="https://localhost")


def test_invalid_scheme():
    with pytest.raises(ValidationError):
        URLInput(original_url="javascript:alert(1)")


def test_domain_without_dot():
    with pytest.raises(ValidationError):
        URLInput(original_url="https://localhost")


def test_valid_mailto():
    data = URLInput(original_url="mailto:test@example.com")
    assert data.original_url.startswith("mailto:")
