"""Application settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-driven settings for the service."""

    app_name: str = "Smart Visual Inspection System"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 60
    jwt_algorithm: str = "HS256"
    database_url: str = "sqlite+aiosqlite:///./svis.db"
    redis_url: str = "redis://redis:6379/0"
    max_file_size_bytes: int = 10 * 1024 * 1024
    allowed_mime_types: tuple[str, ...] = (
        "image/jpeg",
        "image/png",
        "image/webp",
    )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
