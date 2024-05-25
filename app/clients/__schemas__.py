from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field


class CasClientUserDataValidation(PydanticBaseModel):
    """Объект для валидации данных пользователя CAS."""

    phone: str | None = Field(..., regex=r"^\d{10}$")
    cas_id: int | None = Field(..., gt=0)
