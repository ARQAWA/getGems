import asyncio
from typing import TypeVar

import uvloop

from app.core.settings import conf
from app.modules.workers.base_worker import BaseAsyncWorker

Worker = TypeVar("Worker", bound=BaseAsyncWorker)


class WorkerRunner:
    """Класс для запуска воркеров."""

    def __init__(self, worker: Worker) -> None:
        self._worker = worker
        self._message = f"Запуск воркера {self._worker.__class__.__name__}...\n"
        (asyncio if conf.is_local_env else uvloop).run(self.__run())

    async def __run(self) -> None:
        """Бесконечный цикл для запуска воркера."""
        event_loop = asyncio.get_event_loop()
        event_loop.run_in_executor(None, print, self._message)

        # noinspection PyAsyncCall
        event_loop.create_task(self._worker.run())

        while True:
            await asyncio.sleep(86400)  # 24 часа
