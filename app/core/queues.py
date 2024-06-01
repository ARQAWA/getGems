from asyncio import Queue

from app.core.models.nft_collections import NftCollection
from app.core.schemas.get_gems_client import FetchTopCollsRequest

QUEUE_FOR_FETCH: Queue[FetchTopCollsRequest] = Queue()
QUEUE_FOR_CH_INSERT: Queue[NftCollection] = Queue()


__all__ = ["QUEUE_FOR_FETCH", "QUEUE_FOR_CH_INSERT"]
