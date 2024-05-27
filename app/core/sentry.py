import logging

import sentry_sdk
from sentry_sdk.integrations.httpx import HttpxIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from app.core.settings import SentrySettings


def sentry_init(config: SentrySettings) -> None:
    """Инициализация Sentry."""
    logging_integration = LoggingIntegration(
        level=logging.CRITICAL,
        event_level=logging.CRITICAL,
    )

    sentry_sdk.init(
        dsn=config.dsn,
        integrations=[
            HttpxIntegration(),
            logging_integration,
        ],
    )
