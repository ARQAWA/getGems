import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Never, TypeVar

import sentry_sdk

__all__ = ["BaseAsyncWorker", "TAsyncWorker"]

import uvloop
from fast_depends import Depends, inject

# noinspection PyProtectedMember
from app.core._libs import LibsContainer
from app.core.settings import conf

logger = logging.getLogger(__name__)
TAsyncWorker = TypeVar("TAsyncWorker", bound="BaseAsyncWorker")


class BaseAsyncWorker(ABC):
    """Базовый класс для асинхронных воркеров."""

    _cycle_sleeper = 0.5

    @abstractmethod
    async def main(self) -> None:
        """Точка входа для воркера."""
        raise NotImplementedError

    async def _start(self) -> Never:
        """Запуск воркера - основной цикл."""
        while True:
            try:
                await self.main()
                if self._cycle_sleeper > 0:
                    await asyncio.sleep(self._cycle_sleeper)
            except Exception as exc:
                logger.error(f"Failed to run worker!\n{repr(exc)}\nRestarting in 30 seconds...")
                sentry_sdk.capture_exception(exc)
                await asyncio.sleep(30)

    @classmethod
    async def _run(cls) -> None:
        """Запуск воркера - внутренний интерфейс."""

        @inject
        async def _dep(instance: "BaseAsyncWorker" = Depends(cls)) -> None:
            await getattr(instance, "_start")()

        await _dep()

    @classmethod
    def bootstrap(cls) -> None:
        """Запуск воркера - внешний интерфейс."""
        if not conf.is_local_env:
            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

        event_loop = asyncio.new_event_loop()

        try:
            event_loop.create_task(cls._run())
            event_loop.run_forever()
        finally:
            for task in asyncio.all_tasks(event_loop):
                task.cancel()
            event_loop.run_until_complete(LibsContainer.shutdown())
            event_loop.stop()
            event_loop.close()

    @classmethod
    async def background(cls) -> None:
        """Запуск воркера в фоне - внешний интерфейс."""
        asyncio.get_event_loop().create_task(cls._run())  # noqa
