-- Clickhouse create user table
CREATE TABLE IF NOT EXISTS user
(
    id UInt64,
    name String,
    age UInt8
)
ENGINE = MergeTree()
ORDER BY id;