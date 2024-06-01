from datetime import datetime
from decimal import Decimal
from typing import Annotated

from fast_depends import Depends

from app.core.database.clickhouse import ChPool
from app.core.schemas.get_gems_client import KindStr

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

RecordsTuple = tuple[
    tuple[
        str,  # address
        str,  # name
        KindStr,  # period
        int,  # place
        Decimal | None,  # diff
        Decimal,  # ton_value
        Decimal,  # ton_floor_price
        Decimal,  # usd_value
        Decimal,  # usd_floor_price
    ],
    ...,
]


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

    async def insert_many_stat_records(self, records: RecordsTuple) -> None:
        """Вставка записей статистики."""
        if not records:
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
