from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./app.db"
    repo_path: str = "/app/repo/moneyflows-product-specs"
    git_remote_url: str = "https://github.com/JuanPedrajas/mf-product-specs-mock.git"
    git_token: str = ""

    model_config = SettingsConfigDict(env_prefix="APP_")


@lru_cache
def get_settings() -> Settings:
    return Settings()
