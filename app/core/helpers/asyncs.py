import asyncio
from typing import Any, Callable

from app.core.executors import THREAD_XQTR


async def in_thread(func: Callable[..., Any], *args: Any) -> Any:
    """Декоратор для преобразования синхронной функции в асинхронную."""
    return await asyncio.get_event_loop().run_in_executor(
        THREAD_XQTR,
        func,
        *args,
    )
