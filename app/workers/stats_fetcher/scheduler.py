import asyncio
from datetime import UTC, datetime, timedelta

from app.core.clients.getgems_io.schemas import KindStr
from app.core.constants import TIME_MINUTE
from app.core.executors import THREAD_XQTR
from app.core.queues import QUEUE_FOR_FETCH_COLLECTION
from app.workers.base_worker import BaseAsyncWorker

CONST_HOUR_MINUTES = 60
CONST_WAITER_MINUTES = 22
CONST_WAITER_SECONDS = CONST_WAITER_MINUTES * TIME_MINUTE


class StatsFetcherScheduler(BaseAsyncWorker):
    """Класс для планирования работы воркера StatsFetcher."""

    _cycle_sleeper = 0
    _kinds: tuple[KindStr, ...] = ("day", "week", "month", "all")

    async def startup(self) -> None:
        """Код, который выполняется при старте воркера."""
        await self._sleep_on_startup()

    async def main(self) -> None:
        """Код воркеа."""
        await self._execute_pipeline()
        await self._sleep_until_next_hour()

    async def _execute_pipeline(self) -> None:
        """
        Выполнить пайплайн.

        1. Создаем задачи на парсинг данных
        2. Отправляем их в очередь
        3. Спим 5 секунд для того, чтобы все задачи начали выполняться
        """
        for kind in self._kinds:
            await QUEUE_FOR_FETCH_COLLECTION.put((kind, 100, None))

        await asyncio.sleep(3)

    @staticmethod
    async def _sleep_until_next_hour() -> None:
        """Спать до следующего часа."""
        now = datetime.now(UTC)
        next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        if (sleeper := int((next_hour - now).total_seconds()) + 1) > 0:
            asyncio.get_event_loop().run_in_executor(
                THREAD_XQTR,
                print,
                f"StatsFetcherScheduler: next round in " f"{sleeper // TIME_MINUTE:02d}:{sleeper % TIME_MINUTE:02d}",
            )
            await asyncio.sleep(sleeper)

    @staticmethod
    async def _sleep_on_startup() -> None:
        """
        Досыпаем до следующего часа, чтобы начать работу в начале часа.

        Если воркер запущен в начале часа, то он начнет работу сразу.
        """
        now = datetime.now(UTC)

        sleeper = (CONST_HOUR_MINUTES - now.minute) * TIME_MINUTE + now.second
        if sleeper < CONST_WAITER_SECONDS:
            asyncio.get_event_loop().run_in_executor(
                THREAD_XQTR,
                print,
                f"StatsFetcherScheduler: start in " f"{sleeper // TIME_MINUTE:02d}:{sleeper % TIME_MINUTE:02d}",
            )
            await asyncio.sleep(sleeper)
