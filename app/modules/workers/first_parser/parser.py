import asyncio
import logging
from typing import Literal

from app.modules.clients import GetGemsClient
from app.modules.workers.base_worker import BaseAsyncWorker

logger = logging.getLogger(__name__)


class FirstParser(BaseAsyncWorker):
    """Класс для парсинга данных."""

    def __init__(
        self,
        get_gems_client: GetGemsClient,
    ) -> None:
        super().__init__()
        self._get_gems_client = get_gems_client

    async def run(self) -> None:
        """Запуск парсера."""
        cursors: dict[Literal["day", "week", "month", "all"], int | None] = {
            "day": None,
            "week": None,
            "month": None,
            "all": None,
        }

        while True:
            await self._processor(cursors)
            await asyncio.sleep(0.5)

    async def _processor(self, cursors: dict) -> None:
        """Обработчик данных."""
        try:
            await self._single_round(cursors)

        except Exception as e:
            logger.exception("Failed to get top collections", exc_info=e)
            while True:
                await asyncio.sleep(300)

    async def _single_round(self, cursors: dict) -> None:
        """Одиночный раунд обработки данных."""
        for kind, cursor in cursors.items():
            data = await self._get_gems_client.get_top_collections(
                kind=kind,
                count=100,
                cursor=cursor,
            )
            asyncio.get_event_loop().run_in_executor(
                None,
                print,
                kind,
                data.cursor,
                f"Количество коллекций: {len(data.collections)}",
                cursor,
            )
            cursors[kind] = data.cursor
