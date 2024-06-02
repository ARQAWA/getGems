from asyncio import Lock, Queue
from typing import Generic, TypeVar

from app.core.common.chunked_list import Chunk

T = TypeVar("T")


class ChunkedQueue(Generic[T]):
    """Класс для хранения чанков данных."""

    def __init__(self, chunk_size: int = 1000) -> None:
        """Конструктор класса."""
        self._lock = Lock()
        self._chunk_size = chunk_size

        self._queue: Queue[Chunk[T]] = Queue()
        self._current_chunk: Chunk[T] = self.__create_new_chunk()

    def __create_new_chunk(self) -> Chunk[T]:
        """Создание нового чанка."""
        chunk: Chunk[T] = Chunk(self._chunk_size)
        self._queue.put_nowait(chunk)
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
            current_chunk = self._current_chunk
            self._current_chunk = self.__create_new_chunk()

        return current_chunk
