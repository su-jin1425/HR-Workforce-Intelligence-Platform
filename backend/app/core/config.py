from functools import lru_cache
from typing import Literal

from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "HR Workforce Intelligence Platform"
    environment: Literal["local", "test", "staging", "production"] = "local"
    api_prefix: str = "/api/v1"
    database_url: str = "sqlite+aiosqlite:///./hr_workforce_dev.db"
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str = Field(default="dev-only-change-me", min_length=16)
    access_token_minutes: int = 45
    allowed_origins: list[str] = ["http://localhost:3000"]
    public_api_base_url: HttpUrl | None = None

    microsoft_tenant_id: str | None = None
    microsoft_entra_authority: str = "https://login.microsoftonline.com"
    microsoft_api_audience: str | None = None
    require_plugin_auth: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
