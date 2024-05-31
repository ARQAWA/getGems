from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class SentrySettings(BaseModel):
    """Настройки Sentry."""

    dsn: str


class ClickHouseSettings(BaseModel):
    """Настройки ClickHouse."""

    host: str
    port: int
    user: str
    password: str
    database: str
    pool_min_size: int = 1
    pool_max_size: int = 50


class Settings(BaseSettings):
    """Настройки приложения."""

    debug: bool = False
    is_local_env: bool = False

    sentry: SentrySettings
    clickhouse: ClickHouseSettings

    model_config = SettingsConfigDict(
        frozen=True,
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


conf = Settings()  # type: ignore
