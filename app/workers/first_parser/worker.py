import asyncio
import logging
from typing import Literal

from app.core.dependnecies import ChCursor, GetGemsClient
from app.core.schemas.get_gems_client import GetTopCollsParams
from app.workers.base_worker import BaseAsyncWorker

logger = logging.getLogger(__name__)

KindType = Literal["day", "week", "month", "all"]


class FirstParser(BaseAsyncWorker):
    """Класс для парсинга данных."""

    _cycle_sleeper = 0.5

    _cursors: dict[KindType, int | None] = {"day": None, "week": None, "month": None, "all": None}
    _cursors_max: dict[KindType, int] = {"day": 0, "week": 0, "month": 0, "all": 0}

    def __init__(
        self,
        ch_cursor: ChCursor,
        get_gems_client: GetGemsClient,
    ) -> None:
        super().__init__()
        self._cycle_sleeper = 0.5
        self._ch_cursor = ch_cursor
        self._get_gems_client = get_gems_client

    async def main(self) -> None:
        """Код воркеа."""
        while True:
            await self._ch_cursor.execute("SELECT COUNT(address) FROM nft_collection")
            print(await self._ch_cursor.fetchall())  # noqa
            await asyncio.sleep(1)

        for kind, cursor in self._cursors.items():
            data = await self._get_gems_client.get_top_collections(
                GetTopCollsParams(
                    kind=kind,
                    count=100,
                    cursor=cursor,
                ),
            )

            asyncio.get_event_loop().run_in_executor(
                None,
                print,
                kind,
                data.cursor,
                f"Количество коллекций: {len(data.collections)}",
                cursor,
                f"   |   Max cursor: {self._cursors_max[kind]}",
            )

            if data.cursor is not None:
                self._cursors_max[kind] = max(self._cursors_max[kind], int(data.cursor))

            self._cursors[kind] = data.cursor
