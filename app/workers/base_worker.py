import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Never, TypeVar

import sentry_sdk

__all__ = ["BaseAsyncWorker", "TAsyncWorker"]

import uvloop

from app.core.settings import conf

logger = logging.getLogger(__name__)
TAsyncWorker = TypeVar("TAsyncWorker", bound="BaseAsyncWorker")


class BaseAsyncWorker(ABC):
    """Базовый класс для асинхронных воркеров."""

    _cycle_sleeper = 0.5

    @abstractmethod
    async def _main(self) -> None:
        """Точка входа для воркера."""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def _run() -> None:
        """Запуск воркера - внутренний интерфейс."""
        raise NotImplementedError

    async def start(self) -> Never:
        """Запуск воркера - основной цикл."""
        while True:
            try:
                await self._main()
                await asyncio.sleep(self._cycle_sleeper)
            except Exception as e:
                sentry_sdk.capture_exception(e)
                logger.error(f"Failed to run worker! ({e}) Restarting in 30 seconds...")
                await asyncio.sleep(30)

    @classmethod
    def bootstrap(cls) -> None:
        """Запуск воркера - внешний интерфейс."""
        (asyncio if conf.is_local_env else uvloop).run(cls._run())
