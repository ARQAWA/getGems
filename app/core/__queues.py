from asyncio import Queue

from app.core.models.nft_collections import NftCollection
from app.core.schemas.get_gems_client import GetTopCollsParams

FOR_FETCH_Q: Queue[GetTopCollsParams] = Queue()
FOR_CH_INSERT_Q: Queue[NftCollection] = Queue()


__all__ = ("FOR_FETCH_Q", "FOR_CH_INSERT_Q")
