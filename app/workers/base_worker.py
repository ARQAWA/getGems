from abc import ABC, abstractmethod
from typing import Never


class BaseAsyncWorker(ABC):
    """Базовый класс для асинхронных воркеров."""

    @abstractmethod
    async def run(self) -> Never:
        """Запуск воркера."""
        raise NotImplementedError
