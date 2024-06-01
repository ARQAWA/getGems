import logging

from app.workers.base_worker import BaseAsyncWorker

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class StatsFetcherScheduler(BaseAsyncWorker):
    """Класс для планирования работы воркера StatsFetcher."""

    def __init__(self) -> None:
        super().__init__()
        self._cycle_sleeper = 60

    _cycle_sleeper = 0

    async def main(self) -> None:
        """Код воркеа."""
        logger.info("StatsFetcherScheduler: started")

        while True:
            await self._cycle()
            await self.sleep(self._cycle_sleeper)
