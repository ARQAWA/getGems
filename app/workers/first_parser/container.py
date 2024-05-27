from fast_depends import Depends, inject

from app.clients.getgems_io.client import GetGemsClient
from app.workers.first_parser.parser import FirstParser


@inject
def get_first_parser(
    get_gems_client: GetGemsClient = Depends(GetGemsClient),
) -> FirstParser:
    """Разрешение зависимости для парсера."""
    return FirstParser(get_gems_client=get_gems_client)
