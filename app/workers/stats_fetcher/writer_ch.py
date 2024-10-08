import asyncio

from app.core.logger import logger
from app.core.queues import QUEUE_FOR_CH_INSERT_COLL_INFO, QUEUE_FOR_CH_INSERT_COLL_STAT
from app.core.repositories.nft_collection_stats import NftCollectionStatsRepo
from app.core.repositories.nft_collections import NftCollectionInfoRepo
from app.workers.base_worker import BaseAsyncWorker


class StatsFetcherWriterCh(BaseAsyncWorker):
    """Класс для записи данных о коллекциях в ClickHouse."""

    def __init__(
        self,
        nft_collection_info_repo: NftCollectionInfoRepo,
        nft_collection_stats_repo: NftCollectionStatsRepo,
    ) -> None:
        """Инициализация воркера."""
        super().__init__()
        self._nft_collection_info_repo = nft_collection_info_repo
        self._nft_collection_stats_repo = nft_collection_stats_repo

    async def startup(self) -> None:
        """Код, который выполняется при старте воркера."""
        await asyncio.sleep(5)

    async def main(self) -> None:
        """Код воркеа."""
        while True:
            count = await self._write_info()
            count += await self._write_stats()
            if not count:
                await asyncio.sleep(5)

    async def _write_stats(self) -> int:
        """Запись статистики в ClickHouse."""
        stats = await QUEUE_FOR_CH_INSERT_COLL_STAT.get()
        try:
            if len(stats):
                await self._nft_collection_stats_repo.insert_many_stat_records(stats)
                await logger.info(f"Записано {len(stats)} записей в таблицу nft_collections_stats.")

            return len(QUEUE_FOR_CH_INSERT_COLL_STAT)
        except Exception as err:
            await QUEUE_FOR_CH_INSERT_COLL_STAT.park_chunk_front(stats)
            raise err

    async def _write_info(self) -> int:
        """Запись информации о коллекциях в ClickHouse."""
        info = await QUEUE_FOR_CH_INSERT_COLL_INFO.get()
        try:
            if len(info):
                await self._nft_collection_info_repo.insert_many_info_records(info)
                await logger.info(f"Записано {len(info)} записей в таблицу nft_collections_info.")

            return len(QUEUE_FOR_CH_INSERT_COLL_INFO)
        except Exception as err:
            await QUEUE_FOR_CH_INSERT_COLL_INFO.park_chunk_front(info)
            raise err
