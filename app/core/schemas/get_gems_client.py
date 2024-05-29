from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, Field, PlainSerializer


def int_to_str(value: int) -> str:
    """Преобразование числа в строку."""
    return str(value)


CountInt = Annotated[
    int,
    Field(strict=True, ge=0, le=100),
    BeforeValidator(int),
]
CursorInt = Annotated[
    int,
    Field(strict=True, ge=1),
    BeforeValidator(int),
    PlainSerializer(int_to_str, str, "unless-none"),
]


class GetTopCollsParams(BaseModel):
    """Модель параметров запроса топ коллекций."""

    kind: Literal["day", "week", "month", "all"]
    count: CountInt = 100
    cursor: CursorInt | None = None
