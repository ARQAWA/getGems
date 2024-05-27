import asyncio

from app.clients.getgems_io.client import GetGemsClient
from app.workers.base_worker import BaseAsyncWorker


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
        cursor = None

        while True:
            await self._get_gems_client.get_top_collections(kind="day", count=100, cursor=cursor)

            await asyncio.sleep(0.5)
