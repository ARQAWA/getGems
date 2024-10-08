from asyncio import Lock
from collections import deque
from typing import Generic, TypeVar

from app.core.common.chunked_list import Chunk
from app.core.common.retryable import Retryable
from app.core.helpers.retries import helper__item_can_retry

T = TypeVar("T")


class ChunkedQueue(Generic[T], Retryable):
    """Класс для хранения чанков данных."""

    def __init__(self, chunk_size: int, *, max_tries: int) -> None:
        """Конструктор класса."""
        self._chunk_size = chunk_size
        self._max_tries = max_tries
        self._lock = Lock()

        self._deque: deque[Chunk[T]] = deque()
        self._current_chunk: Chunk[T] = self.__create_new_chunk()

    def __create_new_chunk(self) -> Chunk[T]:
        """Создание нового чанка."""
        chunk: Chunk[T] = Chunk(self._chunk_size)
        self._deque.append(chunk)
        return chunk

    async def put(self, item: T) -> None:
        """Добавление элемента в чанк."""
        async with self._lock:
            if self._current_chunk.is_full:
                self._current_chunk = self.__create_new_chunk()

            self._current_chunk.append(item)

    async def get(self) -> Chunk[T]:
        """Получение чанка."""
        async with self._lock:
            first_chunk = self._deque.popleft()
            if not self._deque:
                self._current_chunk = self.__create_new_chunk()

        return first_chunk

    async def park_chunk_front(self, chunk: Chunk[T]) -> None:
        """Парковка чанка в начало."""
        async with self._lock:
            if helper__item_can_retry(self, chunk):
                self._deque.appendleft(chunk)

    def __len__(self) -> int:
        """Получение количества элементов в очереди."""
        return (len(self._deque) - 1) * self._chunk_size + len(self._current_chunk)  # noqa
