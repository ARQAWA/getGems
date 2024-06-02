import asyncio
from functools import partial

from app.core.executors import PROCESS_XQTR
from app.core.schemas.ch_top_colls import TopCollChunkCH, TopCollInfoItemCH, TopCollStatItemCH
from app.core.schemas.get_gems_client import KindStr, ResponseTopColls, TopCollStatItem


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


def __item_to_tuple_double(
    item: TopCollStatItem,
    period: KindStr,
) -> tuple[TopCollStatItemCH, TopCollInfoItemCH]:
    return (
        (
            item["collection"]["address"],
            item["collection"]["name"],
            period,
            item["place"],
            str(item["diffPercent"]) if item["diffPercent"] is not None else None,
            item["tonValue"],
            str(item["floorPrice"]),
            str(item["currencyValue"]),
            str(item["currencyFloorPrice"]),
        ),
        (
            item["collection"]["address"],
            item["collection"]["name"],
            item["collection"]["domain"],
            item["collection"]["isVerified"],
            item["collection"]["approximateHoldersCount"],
            item["collection"]["approximateItemsCount"],
        ),
    )


def refactor_top_colls_answer_sync(
    response: ResponseTopColls,
) -> TopCollChunkCH:
    """Переработка ответа от GetGems API."""
    rework = partial(__item_to_tuple_double, period=response["period"])
    return tuple(map(rework, response["items"]))
