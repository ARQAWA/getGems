from asyncio import Queue

from app.core.common.chunked_queue import ChunkedQueue
from app.core.schemas.ch_top_colls import TopCollInfoItemCH, TopCollStatItemCH
from app.core.schemas.get_gems_client import FetchTopCollsRequest

QUEUE_FOR_FETCH_COLLECTION: Queue[FetchTopCollsRequest] = Queue()
QUEUE_FOR_FETCH_HISTORY: Queue[FetchTopCollsRequest] = Queue()

QUEUE_FOR_CH_INSERT_COLL_STAT: ChunkedQueue[TopCollStatItemCH] = ChunkedQueue()
QUEUE_FOR_CH_INSERT_COLL_INFO: ChunkedQueue[TopCollInfoItemCH] = ChunkedQueue()

__all__ = [
    "QUEUE_FOR_FETCH_COLLECTION",
    "QUEUE_FOR_CH_INSERT_COLL_STAT",
    "QUEUE_FOR_CH_INSERT_COLL_INFO",
    "QUEUE_FOR_FETCH_HISTORY",
]
