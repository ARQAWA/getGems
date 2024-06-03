from typing import Generic, TypeVar

T = TypeVar("T")


class Chunk(list[T], Generic[T]):
    """
    Класс для хранения чанка данных.

    При заполнении чанка, он становится недоступным для изменения.
    """

    def __init__(self, chunk_size: int = 1000) -> None:
        """Конструктор класса."""
        super().__init__([None] * chunk_size)  # type: ignore
        self._capacity = chunk_size
        self._chunk_size = 0

    def append(self, item: T) -> None:
        """Добавление элемента в чанк."""
        if self._chunk_size == self._capacity:
            raise RuntimeError("Chunk is full")

        self[self._chunk_size] = item
        self._chunk_size += 1

    @property
    def is_full(self) -> bool:
        """Проверка на заполненность чанка."""
        return self._chunk_size == self._capacity

    def __len__(self) -> int:
        """Получение длинны чанка."""
        return self._chunk_size

    def pop(self, __index: int = -1):  # type: ignore # noqa
        """Удаление элемента из чанка."""
        raise RuntimeError("You can't pop from chunk")

    def clear(self) -> None:  # noqa # type: ignore
        """Очистка чанка."""
        raise RuntimeError("You can't clear chunk")

    def remove(self, __value: T) -> None:  # noqa # type: ignore
        """Удаление элемента из чанка."""
        raise RuntimeError("You can't remove from chunk")


__all__ = ["Chunk"]
