from fast_depends import Depends, inject

from app.workers.first_parser.worker import FirstParser


@inject
def get_first_parser(
    first_parser: FirstParser = Depends(FirstParser),
) -> FirstParser:
    """Разрешение зависимости для парсера."""
    return first_parser
