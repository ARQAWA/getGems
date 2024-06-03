from decimal import Decimal

from app.core.schemas.get_gems_client import KindStr

TopCollInfoItemCH = tuple[
    str,  # address
    str,  # name
    str | None,  # domain
    bool | None,  # isVerified
    int,  # approximateHoldersCount
    int,  # approximateItemsCount
]

TopCollStatItemCH = tuple[
    str,  # address
    str,  # name
    KindStr,  # period
    int,  # place
    Decimal | None,  # diff
    str,  # tonValue
    Decimal,  # tonFloorPrice
    Decimal,  # currencyValue
    Decimal,  # currencyFloorPrice
]

TopCollChunkCH = tuple[
    tuple[TopCollStatItemCH, TopCollInfoItemCH],
    ...,
]
