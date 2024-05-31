from datetime import datetime
from typing import Optional

from clickhouse_sqlalchemy import make_session, types
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

from app.core.settings import conf

engine = create_engine(
    conf.clickhouse.dsn,
    echo=True,
    echo_pool=True,
    pool_size=10,
    pool_recycle=3600,
    pool_timeout=10,
    pool_pre_ping=True,
    pool_use_lifo=True,
)
session = make_session(engine)
Base = declarative_base()


class NFTCollection(Base):
    """ORM модель для таблицы nft_collection."""

    __tablename__ = "nft_collection"

    address: Mapped[str] = mapped_column(types.String, primary_key=True)
    name: Mapped[str] = mapped_column(types.String)
    domain: Mapped[Optional[str]] = mapped_column(types.Nullable(types.String))
    is_verified: Mapped[Optional[bool]] = mapped_column(types.Nullable(types.UInt8))
    holders_count: Mapped[int] = mapped_column(types.Int32)
    items_count: Mapped[int] = mapped_column(types.Int32)
    created_at: Mapped[datetime] = mapped_column(types.DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(types.DateTime, server_default=func.now())
