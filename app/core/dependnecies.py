from typing import Annotated

from asynch.cursors import Cursor as CursorOrigin
from fast_depends import Depends

from app.core.clients.getgems_io.client import GetGemsClient as GetGemsClientOrigin
from app.core.database.clickhouse import resolve_ch_cursor

GetGemsClient = Annotated[GetGemsClientOrigin, Depends(GetGemsClientOrigin)]
ChCursor = Annotated[CursorOrigin, Depends(resolve_ch_cursor)]

__all__ = ["GetGemsClient", "ChCursor"]
