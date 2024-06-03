from typing import Annotated

from fast_depends import Depends

from app.core.database.clickhouse import ChPool
from app.core.schemas.ch_top_colls import TopCollInfoItemCH

query_insert_info_record = """
INSERT INTO nft_collection
(address, name, domain, is_verified, holders_count, items_count)
VALUES
"""

InfoRecords = list[TopCollInfoItemCH]


class NftCollectionInfoRepoOrigin:
    """Репозиторий для работы с данными информации о коллекциях NFT."""

    def __init__(self, ch_pool: ChPool) -> None:
        """Инициализация репозитория."""
        self._ch_pool = ch_pool

    async def insert_many_info_records(self, records: InfoRecords) -> None:
        """Вставка записей статистики."""
        if not len(records):
            return

        async with self._ch_pool.cursor() as cur:  # type: ChPool.Cursor
            await cur.execute(query_insert_info_record, records)


NftCollectionInfoRepo = Annotated[
    NftCollectionInfoRepoOrigin,
    Depends(NftCollectionInfoRepoOrigin),
]

__all__ = [
    "NftCollectionInfoRepo",
]
