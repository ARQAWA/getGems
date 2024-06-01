from httpx import AsyncClient, Limits, Timeout

from app.core._libs import ObjectCapsule


class HttpxCl(ObjectCapsule[AsyncClient]):
    """Капсула для httpx.Client."""

    @staticmethod
    def _init() -> AsyncClient:
        """Инициализация ресурсов."""
        return AsyncClient(
            limits=Limits(
                max_connections=100,
                max_keepalive_connections=70,
                keepalive_expiry=600,
            ),
            timeout=Timeout(
                timeout=7,
                connect=2,
            ),
        )

    @classmethod
    async def _close(cls) -> None:
        """Закрытие ресурсов."""
        await cls._instance.aclose()  # type: ignore
