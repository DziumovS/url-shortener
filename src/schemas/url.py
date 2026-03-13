from pydantic import BaseModel, field_validator, Field

from src.validators.url_validator import is_valid_url


class URLInput(BaseModel):
    original_url: str = Field(..., min_length=3, max_length=2048)

    @field_validator("original_url")
    def validate_url(cls, v: str) -> str:
        v = v.strip()

        if not is_valid_url(v):
            raise ValueError("Invalid URL")

        return v
