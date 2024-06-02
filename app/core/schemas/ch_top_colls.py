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
    str | None,  # diff
    str,  # tonValue
    str,  # tonFloorPrice
    str,  # currencyValue
    str,  # currencyFloorPrice
]

TopCollChunkCH = tuple[
    tuple[TopCollStatItemCH, TopCollInfoItemCH],
    ...,
]
