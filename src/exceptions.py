class ShortenerError(Exception):
    pass


class NoOriginalUrlFoundError(ShortenerError):
    pass


class SlugAlreadyExistsError(ShortenerError):
    pass
