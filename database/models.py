from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ShortURL(Base):
    __tablename__ = "short_url"

    slug: Mapped[str] = mapped_column(primary_key=True)
    original_url: Mapped[str]
