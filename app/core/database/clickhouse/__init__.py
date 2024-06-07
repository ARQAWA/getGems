from typing import Annotated

import sentry_sdk
from fast_depends import Depends

# noinspection PyProtectedMember
from app.core._libs.clickhouse_pool import ClickhousePool, Pool


async def resolve_ch_pool() -> Pool:
    try:
        pool = ClickhousePool.instance()
        await pool.init()
        return pool
    except Exception as err:
        sentry_sdk.capture_exception(err)
        raise


ChPool = Annotated[Pool, Depends(resolve_ch_pool)]

__all__ = ["ChPool"]
