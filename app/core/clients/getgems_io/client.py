from typing import Any, Literal

import orjson

from app.core.clients import BaseClient, Response
from app.core.models.nft_collections import NftCollectionsResponse
from app.core.schemas.get_gems_client import GetTopCollsParams

from .constants import COLLECTIONS_EXTENSION_STR
from .helpers.collections import get_processed_collections


class GetGemsClient(BaseClient):
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
    ) -> NftCollectionsResponse:
        """
        Получение топовых коллекций.

        :param params: Параметры запроса.
        :return: Список коллекций.
        """
        variables = params.model_dump(exclude_none=True)

        response = await self._graphql(
            "GET",
            "mainPageTopCollection",
            variables=variables,
            extensions=COLLECTIONS_EXTENSION_STR,
        )

        if response.status_code != 200:
            raise RuntimeError(
                f'Failed to execute GraphQL request {{"code": {response.status_code}, "text": {response.text}}}'
            )

        jres = orjson.loads(response.text)

        if "errors" in jres:
            raise RuntimeError(f'Failed to get top collections {{"errors": {jres["errors"]}}}')

        collections = await get_processed_collections(
            jres["data"]["mainPageTopCollection"]["items"],
            params.kind,
        )

        return NftCollectionsResponse(
            collections=collections,
            cursor=jres["data"]["mainPageTopCollection"]["cursor"],
        )
