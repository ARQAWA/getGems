from typing import Literal

from orjson import orjson

from app.clients import BaseClient, Response

from .constants import COLLECTIONS_EXTENSION_STR
from .models import NftCollection, NftCollectionsResponse, NftCollectionStatRecord


class GetGemsClient(BaseClient):
    """Клиент сервиса getgems.io."""

    _base_url = "https://api.getgems.io"
    _graphql_path = "/graphql"
    _static_header = {"Content-Type": "application/json; charset=utf-8"}

    async def _graphql(
        self,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD", "TRACE"],
        operation_name: str,
        variables: dict,
        extensions: dict | str | None = None,
        headers: dict | None = None,
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

        if response.status_code != 200:
            raise RuntimeError(
                "Failed to execute GraphQL request "
                f'{{"code": {response.status_code}, '
                f'"json_response": {response.json}}}'
            )

        return response

    async def get_top_collections(
        self,
        kind: Literal["day", "week", "month", "all"],
        count: int = 100,
        cursor: int | None = None,
    ) -> NftCollectionsResponse:
        """
        Получение топовых коллекций.

        :param kind: Период статистики.
        :param count: Количество записей.
        :param cursor: Пагинация.
        :return: Список коллекций.
        """
        variables = {"kind": kind, "count": count}
        if cursor is not None:
            variables["cursor"] = cursor

        response = await self._graphql(
            "GET",
            "mainPageTopCollection",
            variables=variables,
            extensions=COLLECTIONS_EXTENSION_STR,
        )

        return NftCollectionsResponse(
            collections=[
                NftCollection(
                    **col_["collection"],
                    stat_record=NftCollectionStatRecord(**col_),
                )
                for col_ in response.json["data"]["mainPageTopCollection"]["items"]
            ],
            cursor=response.json["data"]["mainPageTopCollection"]["cursor"],
        )
