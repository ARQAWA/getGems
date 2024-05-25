import typing

import httpx

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

from app.core.settings import conf

SINGLETON_CLIENT: httpx.AsyncClient | None = None


def get_singleton_client() -> httpx.AsyncClient:
    """Получение синглтон-клиента."""
    global SINGLETON_CLIENT

    return SINGLETON_CLIENT or (
        SINGLETON_CLIENT := httpx.AsyncClient(
            limits=httpx.Limits(
                max_connections=10,
                max_keepalive_connections=5,
                keepalive_expiry=600,
            ),
            timeout=httpx.Timeout(timeout=7, connect=2),
            verify=not conf.is_local_env,
        )
    )


class BaseClient:
    """Базовый класс для работы с HTTP-клиентом."""

    base_url = ""

    async def request(
        self,
        method: typing.Literal["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD", "TRACE"],
        path: str,
        *,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: typing.Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
    ) -> httpx.Response:
        """
        Метод для отправки запроса.

        :param method: Метод запроса
        :param path: Путь
        :param content: Тело запроса
        :param data: Данные запроса
        :param files: Файлы запроса
        :param json: JSON запроса
        :param params: Параметры запроса
        :param headers: Заголовки запроса
        :param cookies: Куки запроса
        :param auth: Аутентификация
        :param follow_redirects: Следовать за редиректами
        :param timeout: Таймаут запроса
        :param extensions: Расширения запроса
        :return: Ответ от сервера
        """
        if get_singleton_client().is_closed:
            raise RuntimeError("Client is closed")

        if not isinstance(self.base_url, str):
            raise ValueError("`base_url` must be a string")

        if not path.startswith("/"):
            path = f"/{path}"

        return await get_singleton_client().request(
            method=method,
            url=f"{self.base_url}{path}",
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

    @staticmethod
    async def close() -> None:
        """Закрытие сессии клиента."""
        await get_singleton_client().aclose()


__all__ = ("BaseClient",)
