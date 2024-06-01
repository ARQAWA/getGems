from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, PlainSerializer


def int_to_str(value: int) -> str:
    """Преобразование числа в строку."""
    return str(value)


KindStr = Literal["day", "week", "month", "all"]
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
FetchTopCollsRequest = tuple[KindStr, int, int | None]


class GetTopCollsParams(BaseModel):
    """Модель параметров запроса топ коллекций."""

    kind: KindStr
    count: CountInt = 100
    cursor: CursorInt | None = None

    model_config = ConfigDict(frozen=True)

    @classmethod
    def from_fetch_request(cls, fetch_req: FetchTopCollsRequest) -> "GetTopCollsParams":
        """Инициализация модели из запроса."""
        return cls.construct(
            kind=fetch_req[0],
            count=fetch_req[1],
            cursor=fetch_req[2],
        )


__all__ = ["GetTopCollsParams", "KindStr", "FetchTopCollsRequest"]
