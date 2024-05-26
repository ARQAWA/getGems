import asyncio
from typing import TypeVar

import uvloop

from app.workers.base_worker import BaseAsyncWorker

WorkerClass = TypeVar("WorkerClass", bound=type[BaseAsyncWorker])


class WorkerRunner:
    """Класс для запуска воркеров."""

    def __init__(self, worker_class: WorkerClass) -> None:
        self._worker = worker_class()
        self._message = f"Запуск воркера {self._worker.__class__.__name__}...\n"
        uvloop.run(self.__run())

    async def __run(self) -> None:
        """Бесконечный цикл для запуска воркера."""
        event_loop = asyncio.get_event_loop()
        event_loop.run_in_executor(None, print, self._message)

        # noinspection PyAsyncCall
        event_loop.create_task(self._worker.run())

        while True:
            await asyncio.sleep(86400)  # 24 часа
