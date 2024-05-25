from typing import Optional

from clickhouse_sqlalchemy.types import DateTime as ClickhouseDateTime
from clickhouse_sqlalchemy.types import String as ClickhouseString
from clickhouse_sqlalchemy.types import UInt32
from sqlalchemy import Column, DateTime

from app.core.db.clickhouse import Base


class User(Base):
    """Модель пользователя."""

    __tablename__ = "getgems_users"

    id: int = Column("id", UInt32, primary_key=True, index=True)
    name: Optional[str] = Column("name", ClickhouseString, index=True)
    created_at: Optional[DateTime] = Column("created_at", ClickhouseDateTime)
