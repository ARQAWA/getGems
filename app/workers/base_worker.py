import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Never, TypeVar

import sentry_sdk

__all__ = ["BaseAsyncWorker", "TAsyncWorker"]

logger = logging.getLogger(__name__)
TAsyncWorker = TypeVar("TAsyncWorker", bound="BaseAsyncWorker")


class BaseAsyncWorker(ABC):
    """Базовый класс для асинхронных воркеров."""

    _cycle_sleeper = 0.5

    async def start(self) -> Never:
        """Запуск воркера."""
        while True:
            try:
                await self.main()
                await asyncio.sleep(self._cycle_sleeper)
            except Exception as e:
                sentry_sdk.capture_exception(e)
                logger.error(f"Failed to run worker! ({e}) Restarting in 30 seconds...")
                await asyncio.sleep(30)

    @abstractmethod
    async def main(self) -> None:
        """Точка входа для воркера."""
        raise NotImplementedError
