import logging

from app.core.clients.getgems_io.client import GetGemsClient
from app.core.queues import QUEUE_FOR_FETCH
from app.core.schemas.get_gems_client import FetchTopCollsRequest, GetTopCollsParams
from app.workers.base_worker import BaseAsyncWorker

logger = logging.getLogger(__name__)


class StatsFetcher(BaseAsyncWorker):
    """Класс для парсинга данных."""

    def __init__(
        self,
        get_gems_client: GetGemsClient,
    ) -> None:
        self._get_gems_client = get_gems_client

    _cycle_sleeper = 0

    async def startup(self) -> None:
        """Код, который выполняется при старте воркера."""

    async def main(self) -> None:
        """Код воркеа."""
        while True:
            await self._execute_pipeline(
                await QUEUE_FOR_FETCH.get(),
            )

    async def _execute_pipeline(self, fetch_req: FetchTopCollsRequest) -> None:
        """
        Выкачиваем данные GetGems коллекции.

        1. Отправляем запрос на сервер GetGems
        2. Проверяем курсор и длинну полученных данных
        3. Если данные есть, отправляем в очередь следующий запрос
        4. Отправляем данные в очередь для обработки
        """
        self._get_gems_client.get_top_collections(
            GetTopCollsParams(*FetchTopCollsRequest),
        )
        await self._fetch_data(fetch_req)
        logger.info(f"Finish fetching data for {fetch_req}")
