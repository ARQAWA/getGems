from builtins import staticmethod
from typing import Literal

from orjson import orjson

from app.modules.clients import BaseClient, Response

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

        if "errors" in response.json:
            raise RuntimeError("Failed to get top collections " f'{{"errors": {response.json["errors"]}}}')

        counter = {"none_name": 0}

        return NftCollectionsResponse(
            collections=[
                NftCollection(
                    address=(collection := col_)["collection"]["address"],
                    name=(collection_name := self.__get_none_name(collection["collection"]["name"], counter)),
                    domain=col_["collection"]["domain"],
                    isVerified=col_["collection"]["isVerified"],
                    approximateHoldersCount=col_["collection"]["approximateHoldersCount"],
                    approximateItemsCount=col_["collection"]["approximateItemsCount"],
                    stat_record=NftCollectionStatRecord(
                        address=col_["collection"]["address"],
                        name=collection_name,
                        period=kind.upper(),  # noqa
                        place=col_["place"],
                        diffPercent=col_["diffPercent"],
                        tonValue=col_["tonValue"],
                        floorPrice=col_["floorPrice"],
                        currencyValue=col_["currencyValue"],
                        currencyFloorPrice=col_["currencyFloorPrice"],
                    ),
                )
                for col_ in response.json["data"]["mainPageTopCollection"]["items"]
            ],
            cursor=response.json["data"]["mainPageTopCollection"]["cursor"],
        )

    @staticmethod
    def __get_none_name(name: str | None, counter: dict) -> str:
        if name is not None:
            return name
        counter["none_name"] += 1
        return f'#none_name_{counter["none_name"]:08d}'
