from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./app.db"

    model_config = SettingsConfigDict(env_prefix="APP_")


@lru_cache
def get_settings() -> Settings:
    return Settings()
