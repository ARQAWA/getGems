from app.workers.base_worker import BaseAsyncWorker


class FirstParser(BaseAsyncWorker):
    """Класс для парсинга данных."""

    async def run(self) -> None:
        """Запуск парсера."""
