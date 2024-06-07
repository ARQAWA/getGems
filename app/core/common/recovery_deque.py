from collections import deque
from typing import Generic, TypeVar

from app.core.helpers.retries import helper__item_can_retry

T = TypeVar("T")


class RecoveryDeque(Generic[T], deque[T]):
    """Очередь с возможностью повторной обработки элементов."""

    def __init__(self, *, max_tries: int) -> None:
        """Конструктор класса."""
        super().__init__()
        self._max_tries = max_tries

    def append(self, item: T) -> None:
        """Добавление элемента в очередь."""
        if helper__item_can_retry(item, self._max_tries):
            super().append(item)

    def appendleft(self, item: T) -> None:
        """Добавление элемента в начало очереди."""
        if helper__item_can_retry(item, self._max_tries):
            super().appendleft(item)
