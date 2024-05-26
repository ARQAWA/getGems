from dataclasses import dataclass
from typing import Any, Literal

from orjson import orjson

from app.clients import BaseClient


@dataclass(frozen=True, slots=True)
class Response:
    """DTO ответа от сервиса."""

    status_code: int
    json: Any


class GetGemsClient(BaseClient):
    """Клиент сервиса getgems.io."""

    _base_url = "https://api.getgems.io"
    _graphql_path = "/graphql"
    _static_header = {"Content-Type": "application/json; charset=utf-8"}
    _static_extensions_str = (
        "%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%227"
        "ad7862e974e6b7b96ca883585fca3a86f64ebf4cf00bec9c2f03a8367dfef75%22%7D%7D"
    )

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
            raise RuntimeError("Failed to execute GraphQL request", response.text, response.status_code)

        return Response(status_code=response.status_code, json=orjson.loads(response.text))
