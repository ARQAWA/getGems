import asyncio
from typing import cast

import sentry_sdk
from httpx import HTTPError

from app.core.clients.getgems_io.client import GetGemsClient
from app.core.clients.getgems_io.schemas import FetchTopCollsRequest, GetTopCollsParams
from app.core.executors import THREAD_XQTR
from app.core.logger import logger
from app.core.queues import QUEUE_FOR_CH_INSERT_COLL_INFO, QUEUE_FOR_CH_INSERT_COLL_STAT, QUEUE_FOR_FETCH_COLLECTION
from app.workers.base_worker import BaseAsyncWorker
from app.workers.stats_fetcher.helpers.refactor_top_colls import refactor_top_colls_answer


class StatsFetcherFetcher(BaseAsyncWorker):
    """Класс для скачивания данных о коллекциях."""

    def __init__(
        self,
        get_gems_client: GetGemsClient,
    ) -> None:
        super().__init__()
        self._errors_series = 0
        self._get_gems_client = get_gems_client

    async def startup(self) -> None:
        """Код, который выполняется при старте воркера."""

    async def main(self) -> None:
        """Код воркеа."""
        while True:
            fetch_req = await QUEUE_FOR_FETCH_COLLECTION.get()
            try:
                await self._execute_pipeline(fetch_req)
                self._errors_series = 0
            except Exception as err:
                self._errors_series += 1
                await self.__process_error(err, fetch_req)
            finally:
                if self._errors_series >= 3:
                    self._errors_series = 0
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

        await logger.info(f"StatsFetcherFetcher: {res["cursor"]}/{res["period"]}/items:{len(res["items"])}")

        if res["cursor"] is not None:
            await QUEUE_FOR_FETCH_COLLECTION.put((fetch_req[0], fetch_req[1], cast(int, res["cursor"])))

        ch_ready = await refactor_top_colls_answer(res)

        if res["period"] == "all":
            for stat, info in ch_ready:
                await asyncio.gather(
                    QUEUE_FOR_CH_INSERT_COLL_STAT.put(stat),
                    QUEUE_FOR_CH_INSERT_COLL_INFO.put(info),
                )
        else:
            for stat, _ in ch_ready:
                await QUEUE_FOR_CH_INSERT_COLL_STAT.put(stat)

    @staticmethod
    async def __process_error(err: Exception, fetch_req: FetchTopCollsRequest) -> None:
        if isinstance(err, HTTPError):
            sentry_sdk.capture_message(f"HTTPError in StatsFetcherFetcher: {err}")
            await asyncio.sleep(10)
            await QUEUE_FOR_FETCH_COLLECTION.put(fetch_req)
            asyncio.get_event_loop().run_in_executor(THREAD_XQTR, print, f"HTTPError in StatsFetcherFetcher: {err}")
            return
        else:
            sentry_sdk.capture_exception(err)
            asyncio.get_event_loop().run_in_executor(THREAD_XQTR, print, f"Exception in StatsFetcherFetcher: {err}")
