import asyncio

from app.core.clients.getgems_io.client import GetGemsClient
from app.core.queues import QUEUE_FOR_FETCH
from app.core.schemas.get_gems_client import FetchTopCollsRequest, GetTopCollsParams
from app.workers.base_worker import BaseAsyncWorker


class StatsFetcherFetcher(BaseAsyncWorker):
    """Класс для скачивания данных о коллекциях."""

    def __init__(
        self,
        get_gems_client: GetGemsClient,
    ) -> None:
        self._get_gems_client = get_gems_client

    _cycle_sleeper = 0
    _errors_series = 0

    async def startup(self) -> None:
        """Код, который выполняется при старте воркера."""

    async def main(self) -> None:
        """Код воркеа."""
        while True:
            try:
                await self._execute_pipeline(await QUEUE_FOR_FETCH.get())
            except RuntimeError as err:
                print(f"RuntimeError in StatsFetcherFetcher: {err}")  # noqa
                self._errors_series += 1
                if self._errors_series == 3:
                    await asyncio.sleep(20)

    async def _execute_pipeline(self, fetch_req: FetchTopCollsRequest) -> None:
        """
        Выкачиваем данные GetGems коллекции.

        1. Отправляем запрос на сервер GetGems
        2. Проверяем курсор и длинну полученных данных
        3. Если данные есть, отправляем в очередь следующий запрос
        4. Отправляем данные в очередь для обработки
        """
        res = await self._get_gems_client.get_top_collections(
            GetTopCollsParams.from_fetch_request(fetch_req),
        )

        printer = (res["cursor"], len(res["items"]), res["period"])

        print(f"Got response from GetGems: {printer}")  # noqa
        # if res["cursor"] is not None:
        #     await QUEUE_FOR_FETCH.put((fetch_req[0], fetch_req[1], res["cursor"]))
