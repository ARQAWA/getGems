import asyncio
import logging
from typing import Any, Callable

from app.core.executors import THREAD_XQTR


class AsyncLogger:
    """Класс для асинхронного логгирования."""

    def __init__(self, name: str, level: int) -> None:
        """Инициализация логгера."""
        self._logger = logging.Logger(name, level)

    @staticmethod
    async def _execute(func: Callable[..., Any], *args: Any) -> None:
        """Выполнение функции в отдельном потоке."""
        return await asyncio.get_event_loop().run_in_executor(THREAD_XQTR, func, *args)

    async def info(self, msg: str, *args: Any) -> None:
        """Логгирование информационного сообщения."""
        await self._execute(self._logger.info, msg, *args)

    async def error(self, msg: str, *args: Any) -> None:
        """Логгирование сообщения об ошибке."""
        await self._execute(self._logger.error, msg, *args)


logger = AsyncLogger("async_logger", level=logging.INFO)
