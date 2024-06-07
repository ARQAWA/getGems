from asyncio import Queue
from typing import Generic, TypeVar

from app.core.helpers.retries import helper__item_can_retry

T = TypeVar("T")


class RecoveryQueue(Queue[T], Generic[T]):
    """Очередь с возможностью повторной обработки элементов."""

    def __init__(self, *, max_tries: int) -> None:
        """Конструктор класса."""
        super().__init__()
        self._max_tries = max_tries

    async def put(self, item: T) -> None:
        """Добавление элемента в очередь."""
        if helper__item_can_retry(item, self._max_tries):
            await super().put(item)
