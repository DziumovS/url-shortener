import string
from secrets import choice


SYMBOLS: str = string.ascii_letters + string.digits


def generate_random_slug(length: int = 6) -> str:
    return "".join(choice(SYMBOLS) for _ in range(length))
