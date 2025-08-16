from pydantic import Field
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "Todo API"
    environment: str = Field("dev", validation_alias="ENVIRONMENT")
    debug: bool = True
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:6902@localhost:5432/todo",
        validation_alias="DATABASE_URL",
    )
    jwt_secret: str = Field("supersecret", validation_alias="JWT_SECRET")
    jwt_algorithm: str = "HS256"
    access_token_exp_minutes: int = 30
    rate_limit: str = "20/minute"  # simple global default

    class Config:
        env_file = ".env"
        extra = "ignore"

@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore
