import logging

from app.core.repositories.nft_collection_stats import NftCollectionStatsRepo
from app.workers.base_worker import BaseAsyncWorker

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class StatsFetcherScheduler(BaseAsyncWorker):
    """Класс для планирования работы воркера StatsFetcher."""

    def __init__(self, nft_collection_stats_repo: NftCollectionStatsRepo) -> None:
        self._nft_collection_stats_repo = nft_collection_stats_repo

    _cycle_sleeper = 0

    async def main(self) -> None:
        """Код воркеа."""
        logger.info("StatsFetcherScheduler: started")

        last_updated = await self._nft_collection_stats_repo.get_last_updated()

        if last_updated is None:
            logger.info("StatsFetcherScheduler: no data")
            return
