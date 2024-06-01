import logging

from app.workers.base_worker import BaseAsyncWorker

logger = logging.getLogger(__name__)


class StatsFetcher(BaseAsyncWorker):
    """Класс для парсинга данных."""

    _cycle_sleeper = 999

    async def main(self) -> None:
        """Код воркеа."""
