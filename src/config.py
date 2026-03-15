from pydantic_settings import BaseSettings


class Config(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_EXTERNAL_PORT: str
    POSTGRES_INTERNAL_PORT: str

    REDIS_DB: int
    REDIS_HOST: str
    REDIS_EXTERNAL_PORT: str
    REDIS_INTERNAL_PORT: str

    REDIS_TTL_SECONDS: int

    class Config:
        env_file = ".env"


config = Config()
