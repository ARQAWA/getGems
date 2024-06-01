from dataclasses import dataclass
from typing import Any, Literal

# noinspection PyProtectedMember
from httpx._client import USE_CLIENT_DEFAULT, UseClientDefault  # noqa: PLC2701

# noinspection PyProtectedMember
from httpx._types import (
    AuthTypes,
    CookieTypes,
    HeaderTypes,
    QueryParamTypes,
    RequestContent,
    RequestData,
    RequestExtensions,
    RequestFiles,
    TimeoutTypes,
)

# noinspection PyProtectedMember
from app.core._libs.httpx_client import HttpxCl


@dataclass(frozen=True, slots=True)
class Response:
    """DTO ответа от сервиса."""

    status_code: int
    text: str


class BaseClient:
    """Базовый класс для работы с HTTP-клиентом."""

    _base_url = ""

    def __init__(self) -> None:
        self._httpx_client = HttpxCl.instance()

    async def _request(
        self,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD", "TRACE"],
        path: str,
        *,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
    ) -> Response:
        """Метод для отправки запроса."""
        if self._httpx_client.is_closed:
            raise RuntimeError("Client is closed")

        if not isinstance(self._base_url, str):
            raise ValueError("`base_url` must be a string")

        if not path.startswith("/"):
            path = f"/{path}"

        response = await self._httpx_client.request(
            method=method,
            url=f"{self._base_url}{path}",
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
        )

        return Response(
            status_code=response.status_code,
            text=response.text,
        )


__all__ = ["BaseClient", "Response"]
