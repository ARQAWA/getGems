import sentry_sdk
from sentry_sdk.integrations.httpx import HttpxIntegration

from app.core.settings import SentrySettings


def sentry_init(config: SentrySettings) -> None:
    """Инициализация Sentry."""
    sentry_sdk.init(
        dsn=config.dsn,
        integrations=[
            HttpxIntegration(),
        ],
    )
