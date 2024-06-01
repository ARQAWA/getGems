import asyncio
import contextlib
from asyncio import CancelledError
from typing import Annotated, AsyncGenerator

import asynch
from asynch.connection import Connection  # noqa
from asynch.cursors import Cursor as CursorOrigin
from asynch.pool import Pool as PoolOrigin
from fast_depends import Depends

from app.core.settings import conf


class Pool:
    """Наш пул соединений к ClickHouse."""

    Cursor = CursorOrigin
    _pool: PoolOrigin

    def __init__(self) -> None:
        self.__ready = False
        self.__lock = asyncio.Lock()
        self._pool = PoolOrigin()

    async def init(self) -> None:
        """Инициализация пула соединений."""
        async with self.__lock:
            if not self.__ready:
                self.__ready = True
                self._pool = await asynch.create_pool(
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
                )

    async def close(self) -> None:
        """Закрытие пула соединений."""
        if self.__ready:
            self._pool.close()
            await self._pool.wait_closed()

    @contextlib.asynccontextmanager
    async def cursor(self) -> CursorOrigin:
        """Контекстный менеджер для работы с курсором."""
        async with self._pool.acquire() as conn:  # type: Connection # noqa
            async with conn.cursor() as cursor:
                yield cursor


CH_POOL = Pool()


async def resolve_ch_pool() -> AsyncGenerator[Pool, None]:
    """Зависимость для работы с Pool ClickHouse."""
    await CH_POOL.init()

    try:
        yield CH_POOL
    except (KeyboardInterrupt, SystemExit, CancelledError) as exc:
        await CH_POOL.close()
        raise exc


ChPool = Annotated[Pool, Depends(resolve_ch_pool)]


__all__ = ["ChPool"]
