import asyncio
from typing import Any

from app.core.executors import PROCESS_XQTR
from app.core.models.nft_collections import NftCollection, NftCollectionStatRecord, StatRecordPeriodEnum

__all__ = ("get_processed_collections",)


async def get_processed_collections(input_data: list[dict[str, Any]], kind: str) -> list[NftCollection]:
    """Получение коллекций."""
    period = StatRecordPeriodEnum(kind.upper())
    data = await asyncio.get_event_loop().run_in_executor(
        PROCESS_XQTR,
        get_prepaired_data,
        input_data,
    )

    return [
        NftCollection(
            address=col_["address"],
            name=col_["name"],
            domain=col_["domain"],
            isVerified=col_["isVerified"],
            approximateHoldersCount=col_["approximateHoldersCount"],
            approximateItemsCount=col_["approximateItemsCount"],
            stat_record=NftCollectionStatRecord(
                address=col_["stat_record"]["address"],
                name=col_["stat_record"]["name"],
                period=period,
                place=col_["stat_record"]["place"],
                diffPercent=col_["stat_record"]["diffPercent"],
                tonValue=col_["stat_record"]["tonValue"],
                floorPrice=col_["stat_record"]["floorPrice"],
                currencyValue=col_["stat_record"]["currencyValue"],
                currencyFloorPrice=col_["stat_record"]["currencyFloorPrice"],
            ),
        )
        for col_ in data
    ]


def get_prepaired_data(input_data: list[dict[str, Any]]) -> tuple[dict[str, Any], ...]:
    """Вспомогательная функция для подготовки данных."""
    return tuple(
        dict(
            address=(addr := col_["collection"]["address"]),
            name=(col_name := get_none_name(col_["collection"]["name"], addr)),
            domain=col_["collection"]["domain"],
            isVerified=col_["collection"]["isVerified"],
            approximateHoldersCount=col_["collection"]["approximateHoldersCount"],
            approximateItemsCount=col_["collection"]["approximateItemsCount"],
            stat_record=dict(
                address=col_["collection"]["address"],
                name=col_name,
                place=col_["place"],
                diffPercent=col_["diffPercent"],
                tonValue=col_["tonValue"],
                floorPrice=col_["floorPrice"],
                currencyValue=col_["currencyValue"],
                currencyFloorPrice=col_["currencyFloorPrice"],
            ),
        )
        for col_ in input_data
    )


def get_none_name(name: str | None, address: str) -> str:
    """Получение имени коллекции."""
    if name is not None:
        return name

    return f"#NONE_NAME-{hash(address)}"
