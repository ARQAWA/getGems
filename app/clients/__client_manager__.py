from typing import Annotated

import httpx
from fastapi import Depends
from knowledge_base.application.helpers.singleton_meta import SingletonMeta
from knowledge_base.application.settings import conf

__all__ = ("HttpClientManager",)


class HttpClientManager(metaclass=SingletonMeta):
    """Менеджер сессий для клиентов. (Singleton)."""

    __depends__ = Annotated[httpx.AsyncClient, Depends(lambda: HttpClientManager().client)]

    def __init__(self) -> None:
        self._client_instance = httpx.AsyncClient(
            limits=httpx.Limits(
                max_connections=10,
                max_keepalive_connections=5,
                keepalive_expiry=600,
            ),
            timeout=httpx.Timeout(timeout=7, connect=2),
            verify=not conf.is_local_env,
        )

    @property
    def client(self) -> httpx.AsyncClient:
        """Проперти для получения сессии клиента."""
        return self._client_instance

    async def close(self) -> None:
        """Закрытие сессии клиента."""
        await self._client_instance.aclose()
