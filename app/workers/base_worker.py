import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any, Never, TypeVar

import sentry_sdk
import uvloop
from fast_depends import Depends, inject

# noinspection PyProtectedMember
from app.core._libs import LibsContainer
from app.core.settings import conf

LOGGER = logging.getLogger(__name__)
INJECT_LOCK = asyncio.Lock()
TAsyncWorker = TypeVar("TAsyncWorker", bound="BaseAsyncWorker")


class BaseAsyncWorker(ABC):
    """Базовый класс для асинхронных воркеров."""

    _cycle_sleeper = 0.5

    @abstractmethod
    async def startup(self) -> None:
        """Код, который выполняется при старте воркера."""
        raise NotImplementedError

    @abstractmethod
    async def main(self) -> None:
        """Точка входа для воркера."""
        raise NotImplementedError

    async def _start(self) -> Never:
        """Запуск воркера - основной цикл."""
        await self.startup()
        while True:
            try:
                await self.main()
                if self._cycle_sleeper > 0:
                    await asyncio.sleep(self._cycle_sleeper)
            except Exception as exc:
                LOGGER.error(f"Failed to run worker!\n{repr(exc)}\nRestarting in 30 seconds...")
                sentry_sdk.capture_exception(exc)
                await asyncio.sleep(30)

    @classmethod
    async def _run(cls) -> None:
        """Запуск воркера - внутренний интерфейс."""

        @inject
        async def _get_start_coro(instance: "BaseAsyncWorker" = Depends(cls)) -> Any:
            return getattr(instance, "_start")()

        async with INJECT_LOCK:
            start_coro = await _get_start_coro()

        await start_coro

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
    def background(cls, event_loop: asyncio.AbstractEventLoop) -> None:
        """Запуск воркера в фоне - внешний интерфейс."""
        event_loop.create_task(cls._run())  # noqa


__all__ = ["BaseAsyncWorker", "TAsyncWorker"]
