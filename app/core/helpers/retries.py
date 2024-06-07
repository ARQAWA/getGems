from typing import TypeVar

from app.core.common.retryable import Retryable

T = TypeVar("T")
R = TypeVar("R", bound=Retryable)


def helper__item_can_retry(retryable_obj: R, item: T) -> bool:
    """Проверка возможности повторной обработки элемента."""
    max_retries: int | None = getattr(retryable_obj, "_max_tries", None)
    if max_retries is None:
        raise AttributeError(f"Object {retryable_obj} has no attribute '_max_tries'!")

    class_id = abs(id(retryable_obj.__class__))
    object_id = abs(id(retryable_obj))
    attribute_name = f"__{class_id}_{object_id}_retries"
    retries = getattr(item, attribute_name, -1) + 1
    setattr(item, attribute_name, retries)
    return retries <= max_retries
