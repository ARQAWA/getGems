import asyncio
from asyncio import CancelledError
from typing import cast

import asynch
from asynch.connection import Connection  # noqa
from asynch.cursors import Cursor
from asynch.pool import Pool
from fast_depends import Depends

from app.core.settings import conf

CH_POOL: Pool | None = None


async def resolve_ch_pool() -> Pool:
    """Зависимость для работы с Pool ClickHouse."""
    global CH_POOL

    if CH_POOL is None:
        CH_POOL = cast(
            Pool,
            await asynch.create_pool(
                conf.clickhouse.pool_min_size,
                conf.clickhouse.pool_max_size,
                loop=asyncio.get_event_loop(),
                **dict(
                    host=conf.clickhouse.host,
                    port=conf.clickhouse.port,
                    user=conf.clickhouse.user,
                    password=conf.clickhouse.password,
                    database=conf.clickhouse.database,
                ),
            ),
        )

    try:
        yield CH_POOL
    except (KeyboardInterrupt, SystemExit, CancelledError) as exc:
        await CH_POOL.clear()
        raise exc


async def resolve_ch_cursor(pool: Pool = Depends(resolve_ch_pool)) -> Cursor:
    """Зависимость для работы с Cursor ClickHouse."""
    async with pool.acquire() as conn:  # type: Connection # noqa
        async with conn.cursor() as cursor:
            yield cursor


__all__ = ["resolve_ch_cursor", "CH_POOL"]
