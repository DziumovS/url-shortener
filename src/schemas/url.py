from pydantic import BaseModel, field_validator

from src.validators.url_validator import is_valid_url


class URLInput(BaseModel):
    original_url: str

    @field_validator("original_url")
    def check_url(cls, v: str) -> str:
        if not is_valid_url(v):
            raise ValueError("Invalid URL")
        return v
