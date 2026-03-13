from urllib.parse import urlparse
import ipaddress
import idna


ALLOWED_SCHEMES: set[str] = {"http", "https", "ftp", "ftps", "mailto", "tg", "slack", "whatsapp"}

MESSENGER_SCHEMES: set[str] = {"mailto", "tg", "slack", "whatsapp"}


def _is_public_ip(host: str) -> bool:
    try:
        ip = ipaddress.ip_address(host)
        return not (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_reserved
            or ip.is_multicast
        )
    except ValueError:
        return False


def _normalize_hostname(hostname: str) -> str | None:
    try:
        return idna.encode(hostname).decode("ascii")
    except Exception:
        return None


def is_valid_url(url: str) -> bool:
    if not url:
        return False

    try:
        parsed = urlparse(url)
    except Exception:
        return False

    if not parsed.scheme:
        return False

    scheme = parsed.scheme.lower()

    if scheme not in ALLOWED_SCHEMES:
        return False

    if "@" in parsed.netloc:
        return False

    if scheme in MESSENGER_SCHEMES:
        return bool(parsed.netloc or parsed.path)

    hostname = parsed.hostname

    if not hostname:
        return False

    hostname = _normalize_hostname(hostname)

    if not hostname:
        return False

    if hostname == "localhost":
        return False

    if _is_public_ip(hostname) is False:
        try:
            ipaddress.ip_address(hostname)
            return False
        except ValueError:
            pass

    if "." not in parsed.hostname:
        return False

    if parsed.port:
        if parsed.port < 1 or parsed.port > 65535:
            return False

    return True
