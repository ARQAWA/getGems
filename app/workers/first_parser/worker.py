import asyncio
import logging
from datetime import UTC, datetime, timedelta
from typing import Literal

from app.core.clients.getgems_io.client import GetGemsClient
from app.core.repositories.nft_collection_stats import NftCollectionStatsRepo
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
        get_gems_client: GetGemsClient,
        nft_collection_stats_repo: NftCollectionStatsRepo,
    ) -> None:
        self._get_gems_client = get_gems_client
        self._nft_collection_stats_repo = nft_collection_stats_repo

    async def main(self) -> None:
        """Код воркеа."""
        while True:
            res = await self._nft_collection_stats_repo.get_last_updated()

            if res is None:
                print("No data")  # noqa

            else:
                print(f"Last updated: {res}")  # noqa
                next_hour = res.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
                print(f"Next hour: {next_hour}, now: {datetime.now(UTC)}")  # noqa
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
