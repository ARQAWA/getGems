from typing import Annotated

from aiochclient import ChClient as ChClientOrigin
from fast_depends import Depends

from app.core.clients.getgems_io.client import GetGemsClient as GetGemsClientOrigin
from app.core.database.clickhouse import resolve_ch_client

GetGemsClient = Annotated[GetGemsClientOrigin, Depends(GetGemsClientOrigin)]
ChClient = Annotated[ChClientOrigin, Depends(resolve_ch_client)]
