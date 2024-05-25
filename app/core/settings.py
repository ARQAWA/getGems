from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class SentrySettings(BaseModel):
    """Настройки Sentry."""

    dsn: str


class ClickHouseSettings(BaseModel):
    """Настройки ClickHouse."""

    dsn: str

    @field_validator("dsn", mode="before")
    def check_dsn(cls, value: str) -> str:
        """Проверка DSN."""
        if not value.startswith("clickhouse://"):
            raise ValueError("DSN должен начинаться с clickhouse://")
        return value.replace("clickhouse://", "clickhouse+native://")


class Settings(BaseSettings):
    """Настройки приложения."""

    debug: bool = False

    sentry: SentrySettings
    clickhouse: ClickHouseSettings

    model_config = SettingsConfigDict(
        frozen=True,
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


conf = Settings()
