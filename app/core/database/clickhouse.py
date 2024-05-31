from aiochclient import ChClient

from app.core.clients.base_client import ASYNC_HTTPX_CLIENT
from app.core.settings import conf


async def resolve_ch_client() -> ChClient:
    """Зависимость для работы с ClickHouse."""
    client = ChClient(
        ASYNC_HTTPX_CLIENT,
        url=conf.clickhouse.url,
        user=conf.clickhouse.user,
        password=conf.clickhouse.password,
        database=conf.clickhouse.database,
    )

    try:
        yield client
    finally:
        await client.close()


__all__ = ["resolve_ch_client"]
