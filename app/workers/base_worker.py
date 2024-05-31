import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Never, TypeVar

import sentry_sdk

__all__ = ["BaseAsyncWorker", "TAsyncWorker"]

import uvloop
from fast_depends import Depends, inject

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
        (asyncio if conf.is_local_env else uvloop).run(cls._run())
