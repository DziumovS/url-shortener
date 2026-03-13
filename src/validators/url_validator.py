from urllib.parse import urlparse


ALLOWED_SCHEMES: set[str] = {"http", "https", "ftp", "ftps", "mailto", "tg", "slack", "whatsapp"}

MESSENGER_SCHEMES = {"mailto", "tg", "slack", "whatsapp"}


def is_valid_url(url: str) -> bool:
    try:
        parsed = urlparse(url)

        if not parsed.scheme:
            return False

        scheme = parsed.scheme.lower()

        if scheme not in ALLOWED_SCHEMES:
            return False

        if "@" in parsed.netloc:
            return False

        if scheme in MESSENGER_SCHEMES:
            return bool(parsed.netloc or parsed.path)

        if not parsed.netloc:
            return False

        if "." not in parsed.netloc:
            return False

        return True

    except Exception:
        return False
