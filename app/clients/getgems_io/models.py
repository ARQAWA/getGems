from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class NftCollection(BaseModel):
    """Модель NFT коллекции."""

    address: str = Field(description="Адрес коллекции")
    name: str = Field(description="Название коллекции")
    domain: Optional[str] = Field(description="Домен коллекции")
    is_verified: bool = Field(alias="isVerified", description="Проверена ли коллекция")
    holders_count: int = Field(alias="approximateHoldersCount", description="Примерное количество держателей")
    items_count: int = Field(alias="approximateItemsCount", description="Примерное количество предметов")
    updated_at: datetime = Field(description="Дата обновления")
    created_at: datetime = Field(description="Дата создания")


class StatRecordPeriodEnum(str, Enum):
    """Перечисление периодов статистики."""

    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"
    ALL = "ALL"


class NftCollectionStatRecord(BaseModel):
    """Модель записи статистики коллекции."""

    address: str = Field(description="Адрес коллекции")
    name: str = Field(description="Название коллекции")
    period: StatRecordPeriodEnum = Field(description="Период статистики")
    place: int = Field(description="Место в рейтинге")
    diff: Decimal = Field(alias="diffPercent", description="Процент изменения")
    ton_value: Decimal = Field(alias="tonValue", description="TON общая стоимость коллекции")
    ton_floor_price: Decimal = Field(alias="floorPrice", description="TON минимальная цена")
    usd_value: Decimal = Field(alias="currencyValue", description="USD общая стоимость коллекции")
    usd_floor_price: Decimal = Field(alias="currencyFloorPrice", description="USD минимальная цена")
    updated_at: datetime = Field(description="Дата обновления")
    created_at: datetime = Field(description="Дата создания")
