from app.core.dependnecies import ChCursor

query_get_last_updated_date = """
SELECT updated_at
FROM nft_collection_stat
WHERE period = 'day'
ORDER BY updated_at DESC
LIMIT 1
"""

#     address String,
#     name String,
#     period LowCardinality(String),
#     place Int32,
#     diff Decimal(18, 10),
#     ton_value Decimal(18, 10),
#     ton_floor_price Decimal(18, 10),
#     usd_value Decimal(18, 10),
#     usd_floor_price Decimal(18, 10),
#     created_at DateTime DEFAULT now(),
#     updated_at DateTime DEFAULT now()

query_insert_stat_record = """
INSERT INTO nft_collection_stat
(address, name, period, place, diff, ton_value, ton_floor_price, usd_value, usd_floor_price)


class NftCollectionStatsRepository:
    """Репозиторий для работы с данными статистики коллекций NFT."""

    def __init__(self, ch_cursor: ChCursor) -> None:
        self._ch_cursor = ch_cursor

    def get_last_updated(self) -> int | None:
        """Получение времени последнего обновления статистики."""
        self._ch_cursor.execute(query_get_last_updated_date)
        res = self._ch_cursor.fetchone()
        return res[0] if res else None

    def insert_many_stat_records(self, records: list[tuple]) -> None:
        """Вставка записей статистики."""
        self._ch_cursor.executemany(
            """
            INSERT INTO nft_collection_stat_record
            (collection_id, period, updated_at, data)
            VALUES
            (%s, %s, %s, %s)
            """,
            records,
        )