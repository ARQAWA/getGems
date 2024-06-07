from datetime import datetime
from typing import Annotated

from fast_depends import Depends

from app.core.database.clickhouse import ChPool
from app.core.database.clickhouse.schemas.collections import TopCollStatItemCH

query_get_last_updated_date = """
SELECT created_at
FROM nft_collection_stat
WHERE period = 'day'
ORDER BY created_at DESC
LIMIT 1
"""

query_insert_stat_record = """
INSERT INTO nft_collection_stat
(address, name, period, place, diff, ton_value, ton_floor_price, usd_value, usd_floor_price)
VALUES
"""

StatRecords = list[TopCollStatItemCH]


class NftCollectionStatsRepoOrigin:
    """Репозиторий для работы с данными статистики коллекций NFT."""

    def __init__(self, ch_pool: ChPool) -> None:
        """Инициализация репозитория."""
        self._ch_pool = ch_pool

    async def get_last_updated(self) -> datetime | None:
        """Получение времени последнего обновления статистики."""
        async with self._ch_pool.cursor() as cur:  # type: ChPool.Cursor
            await cur.execute(query_get_last_updated_date)
            res = await cur.fetchone()
        return res[0] if res else None

    async def insert_many_stat_records(self, records: StatRecords) -> None:
        """Вставка записей статистики."""
        if not len(records):
            return

        async with self._ch_pool.cursor() as cur:  # type: ChPool.Cursor
            await cur.execute(query_insert_stat_record, records)


NftCollectionStatsRepo = Annotated[
    NftCollectionStatsRepoOrigin,
    Depends(NftCollectionStatsRepoOrigin),
]

__all__ = [
    "NftCollectionStatsRepo",
]
