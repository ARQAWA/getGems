from typing import TypeVar

T = TypeVar("T")


def helper__item_can_retry(item: T, max_retries: int) -> bool:
    """Проверка возможности повторной обработки элемента."""
    retries = getattr(item, "_retries", -1) + 1
    setattr(item, "_retries", retries)
    return retries <= max_retries
