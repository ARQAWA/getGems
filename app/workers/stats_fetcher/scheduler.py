import asyncio
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

from app.core.constants import TIME_HOUR, TIME_MINUTE
from app.core.queues import QUEUE_FOR_FETCH
from app.core.repositories.nft_collection_stats import NftCollectionStatsRepo
from app.workers.base_worker import BaseAsyncWorker

if TYPE_CHECKING:
    from app.core.schemas.get_gems_client import KindStr

CONST_22_MINUTES = 22 * TIME_MINUTE


class StatsFetcherScheduler(BaseAsyncWorker):
    """Класс для планирования работы воркера StatsFetcher."""

    def __init__(
        self,
        nft_collection_stats_repo: NftCollectionStatsRepo,
    ) -> None:
        self._nft_collection_stats_repo = nft_collection_stats_repo

    _cycle_sleeper = 0

    async def startup(self) -> None:
        """Код, который выполняется при старте воркера."""
        await self._sleep_on_startup()

    async def main(self) -> None:
        """Код воркеа."""
        await self._execute_pipeline()
        await self._sleep_until_next_hour()

    @staticmethod
    async def _execute_pipeline() -> None:
        """
        Выполнить пайплайн.

        1. Создаем задачи на парсинг данных
        2. Отправляем их в очередь
        3. Спим 5 секунд для того, чтобы все задачи начали выполняться
        """
        kinds: tuple[KindStr, ...] = ("day", "week", "month", "all")

        for kind in kinds:
            await QUEUE_FOR_FETCH.put((kind, 100, None))

        await asyncio.sleep(3)

    @staticmethod
    async def _sleep_until_next_hour() -> None:
        """Спать до следующего часа."""
        now = datetime.now(UTC)
        next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)

        await asyncio.sleep((next_hour - now).total_seconds())

    async def _sleep_on_startup(self) -> None:
        """
        Досыпаем до следующего часа, чтобы начать работу в начале часа.

        Если воркер запущен в начале часа, то он начнет работу сразу.
        """
        now = datetime.now(UTC)
        last_updated = await self._nft_collection_stats_repo.get_last_updated()

        if last_updated is None or last_updated < now - timedelta(hours=1):
            last_updated = datetime.now(UTC) - timedelta(hours=1)

        sleeper = (datetime.now(UTC) - last_updated).total_seconds() % TIME_HOUR

        if sleeper < CONST_22_MINUTES:
            print(f"StatsFetcherScheduler: start in {sleeper} seconds")  # noqa
            await asyncio.sleep(sleeper)
