CREATE TABLE IF NOT EXISTS nft_collection_stat
(
    address String,
    name String,
    period LowCardinality(String),
    place Int32,
    diff Decimal(18, 10),
    ton_value Decimal(18, 10),
    ton_floor_price Decimal(18, 10),
    usd_value Decimal(18, 10),
    usd_floor_price Decimal(18, 10),
    created_at DateTime DEFAULT now()
)
ENGINE = MergeTree()
ORDER BY (address, period, created_at);
