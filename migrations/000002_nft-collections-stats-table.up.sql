CREATE TABLE IF NOT EXISTS nft_collection_stat_record
(
    address String,
    period LowCardinality(String),
    place Int32,
    name String,
    diff Decimal(18, 10),
    ton_value Decimal(18, 10),
    ton_floor_price Decimal(18, 10),
    usd_value Decimal(18, 10),
    usd_floor_price Decimal(18, 10),
    created_at DateTime DEFAULT now(),
    updated_at DateTime DEFAULT now()
)
ENGINE = MergeTree()
ORDER BY (address, period, place, updated_at);
