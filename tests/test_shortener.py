from src.shortener import generate_random_slug


def test_generate_random_slug_default() -> None:
    slug = generate_random_slug()

    assert isinstance(slug, str)
    assert len(slug) == 6


def test_generate_random_slug_custom_length() -> None:
    slug = generate_random_slug(10)

    assert len(slug) == 10
