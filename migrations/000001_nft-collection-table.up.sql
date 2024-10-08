CREATE TABLE IF NOT EXISTS nft_collection
(
    address String,
    name String,
    domain Nullable(String),
    is_verified Nullable(Bool),
    holders_count Int32,
    items_count Int32,
    created_at DateTime64(6, 'UTC') DEFAULT now(),
    updated_at DateTime64(6, 'UTC') DEFAULT now()
)
ENGINE = MergeTree()
ORDER BY (address, updated_at);
