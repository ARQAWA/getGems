import asyncio
from decimal import Decimal
from functools import partial

from app.core.clients.getgems_io.schemas import KindStr, ResponseTopColls, TopCollStatItem
from app.core.database.clickhouse.schemas.collections import TopCollChunkCH, TopCollInfoItemCH, TopCollStatItemCH
from app.core.executors import PROCESS_XQTR


async def refactor_top_colls_answer(
    response: ResponseTopColls,
) -> TopCollChunkCH:
    """Переработка ответа от GetGems API."""
    event_loop = asyncio.get_event_loop()
    return await event_loop.run_in_executor(
        PROCESS_XQTR,
        refactor_top_colls_answer_sync,
        response,
    )


def refactor_top_colls_answer_sync(
    response: ResponseTopColls,
) -> TopCollChunkCH:
    """Переработка ответа от GetGems API."""
    rework = partial(__item_to_tuple_double, period=response["period"])
    return tuple(map(rework, response["items"]))


def __item_to_tuple_double(
    item: TopCollStatItem,
    period: KindStr,
) -> tuple[TopCollStatItemCH, TopCollInfoItemCH]:
    return (
        (
            item["collection"]["address"],
            __get_none_name(item["collection"]["name"], item["collection"]["address"]),
            period,
            item["place"],
            Decimal(item["diffPercent"]) if item["diffPercent"] is not None else None,
            item["tonValue"],
            Decimal(item["floorPrice"]),
            Decimal(item["currencyValue"]),
            Decimal(item["currencyFloorPrice"]),
        ),
        (
            item["collection"]["address"],
            __get_none_name(item["collection"]["name"], item["collection"]["address"]),
            item["collection"]["domain"],
            item["collection"]["isVerified"],
            item["collection"]["approximateHoldersCount"],
            item["collection"]["approximateItemsCount"],
        ),
    )


def __get_none_name(name: str | None, address: str) -> str:
    """Получение имени коллекции."""
    if name is not None:
        return name

    return f"#NONE_NAME-{hash(address)}"
