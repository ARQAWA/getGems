from typing import Annotated, Any, Literal

import orjson
from fast_depends import Depends

from app.core.clients import BaseClient, Response
from app.core.clients.getgems_io.constants import COLLECTIONS_EXTENSION_STR
from app.core.clients.getgems_io.schemas import GetTopCollsParams, ResponseTopColls


class GetGemsClientOrigin(BaseClient):
    """Клиент сервиса getgems.io."""

    _base_url = "https://api.getgems.io"
    _graphql_path = "/graphql"
    _static_header = {"Content-Type": "application/json; charset=utf-8"}

    async def _graphql(
        self,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD", "TRACE"],
        operation_name: str,
        variables: dict[str, Any],
        extensions: dict[str, Any] | str | None = None,
        headers: dict[str, Any] | None = None,
    ) -> Response:
        """Выполнение запроса к GraphQL API."""
        headers = headers or {}
        headers.update(self._static_header)

        params = {
            "operationName": operation_name,
            "variables": orjson.dumps(variables).decode(),
        }

        if isinstance(extensions, dict):
            params["extensions"] = orjson.dumps(extensions).decode()
        elif isinstance(extensions, str):
            params["extensions"] = extensions

        response = await self._request(
            method,
            self._graphql_path,
            params=params,
            headers=headers,
        )

        return response

    async def get_top_collections(
        self,
        params: GetTopCollsParams,
    ) -> ResponseTopColls:
        """
        Получение топовых коллекций.

        :param params: Параметры запроса.
        :return: Список коллекций.
        """
        response = await self._graphql(
            "GET",
            "mainPageTopCollection",
            variables=params.model_dump(exclude_none=True),
            extensions=COLLECTIONS_EXTENSION_STR,
        )

        if response.status_code != 200:
            raise RuntimeError("Unexpected response in get top collections", response.status_code, response.text)

        jres = orjson.loads(response.text)

        if not isinstance(jres, dict):
            raise RuntimeError("Unexpected response in get top collections", jres)

        if "errors" in jres:
            raise RuntimeError("Failed to get top collections", jres["errors"])

        if jres.get("data", {}).get("mainPageTopCollection") is None:
            raise RuntimeError("Unexpected response in get top collections", jres)

        return {
            "items": jres["data"]["mainPageTopCollection"]["items"],
            "cursor": jres["data"]["mainPageTopCollection"]["cursor"],
            "period": params.kind,
        }


GetGemsClient = Annotated[GetGemsClientOrigin, Depends(GetGemsClientOrigin)]


__all__ = ["GetGemsClient"]
