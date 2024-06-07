from asyncio import Queue

from app.core.clients.getgems_io.schemas import FetchTopCollsRequest
from app.core.common.chunked_queue import ChunkedQueue
from app.core.database.clickhouse.schemas.collections import TopCollInfoItemCH, TopCollStatItemCH

QUEUE_FOR_FETCH_COLLECTION: Queue[FetchTopCollsRequest] = Queue()

QUEUE_FOR_CH_INSERT_COLL_STAT: ChunkedQueue[TopCollStatItemCH] = ChunkedQueue(5000)
QUEUE_FOR_CH_INSERT_COLL_INFO: ChunkedQueue[TopCollInfoItemCH] = ChunkedQueue(5000)

__all__ = [
    "QUEUE_FOR_FETCH_COLLECTION",
    "QUEUE_FOR_CH_INSERT_COLL_STAT",
    "QUEUE_FOR_CH_INSERT_COLL_INFO",
]
