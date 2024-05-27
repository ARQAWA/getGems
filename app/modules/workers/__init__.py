import asyncio

import uvloop

from app.core.settings import conf

from .base_worker import TAsyncWorker

__all__ = ("run_worker",)


def run_worker(worker: TAsyncWorker) -> None:
    """Запуск воркера."""
    (asyncio if conf.is_local_env else uvloop).run(worker.start())
