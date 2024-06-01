from typing import Annotated

from fast_depends import Depends

# noinspection PyProtectedMember
from app.core._libs.clickhouse_pool import ClickhousePool, Pool


async def resolve_ch_pool() -> Pool:
    pool = ClickhousePool.instance()
    await pool.init()
    return pool


ChPool = Annotated[Pool, Depends(resolve_ch_pool)]

__all__ = ["ChPool"]
