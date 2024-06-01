import asyncio
import logging

from app.workers.base_worker import BaseAsyncWorker
from app.workers.stats_fetcher.fetcher import StatsFetcherFetcher
from app.workers.stats_fetcher.scheduler import StatsFetcherScheduler

logger = logging.getLogger(__name__)


class StatsFetcherMain(BaseAsyncWorker):
    """Класс для парсинга данных."""

    _cycle_sleeper = 999

    async def startup(self) -> None:
        """Код, который выполняется при старте воркера."""
        self._run_workers()

    async def main(self) -> None:
        """Код воркеа."""

    @staticmethod
    def _run_workers() -> None:
        """
        Запуск воркеров.

        1. Запускаем воркер для скачивания данных.
        2. Запускаем воркер плаанировщик.
        """
        event_loop = asyncio.get_event_loop()

        for _ in range(10):
            StatsFetcherFetcher.background(event_loop)

        StatsFetcherScheduler.background(event_loop)
