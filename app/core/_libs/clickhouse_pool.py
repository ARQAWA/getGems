import asyncio
import contextlib

import asynch
import sentry_sdk
from asynch.connection import Connection  # noqa
from asynch.cursors import Cursor as CursorOrigin
from asynch.pool import Pool as PoolOrigin

from app.core._libs import ObjectCapsule
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
                try:
                    yield cursor
                except Exception as err:
                    sentry_sdk.capture_exception(err)
                    raise


class ClickhousePool(ObjectCapsule[Pool]):
    """Капсула для Pool ClickHouse."""

    @staticmethod
    def _init() -> Pool:
        return Pool()

    @classmethod
    async def _close(cls) -> None:
        await cls._instance.close()  # type: ignore


__all__ = ["ClickhousePool", "Pool"]
