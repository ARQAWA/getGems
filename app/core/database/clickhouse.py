import contextlib

from aiochclient import ChClient

from app.core.clients.base_client import get_singleton_client
from app.core.settings import conf


@contextlib.asynccontextmanager
async def resolve_ch_client() -> ChClient:
    """Зависимость для работы с ClickHouse."""
    client = ChClient(
        get_singleton_client(),
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
