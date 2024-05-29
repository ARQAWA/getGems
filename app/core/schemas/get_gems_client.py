from typing import Annotated, Literal

from pydantic import BaseModel, Field

CountInt = Annotated[int, Field(strict=True, ge=0, le=100)]
CursorInt = Annotated[int, Field(strict=True, ge=1)]


class GetTopCollsParams(BaseModel):
    """Модель параметров запроса топ коллекций."""

    kind: Literal["day", "week", "month", "all"]
    limit: CountInt = 100
    cursor: CursorInt | None = None
