from typing import (
    Annotated,
    Any,
    Literal,
)

from fastapi import HTTPException
from knowledge_base.application.auth.model import User
from knowledge_base.application.general.layer_dependency import DependencyLayerBase
from knowledge_base.application.settings import conf
from knowledge_base.entities.cas_user import CasUser

from . import HttpClientManager
from .__schemas__ import CasClientUserDataValidation

__all__ = ("CasClient",)

from knowledge_base.application.helpers.get_full_url import get_full_url


class CasClient(DependencyLayerBase):
    """Клиент для работы с CAS."""

    __depends__ = Annotated["CasClient", None]

    def __init__(
        self,
        user: User.__depends__,
        http_client: HttpClientManager.__depends__,
    ) -> None:
        self._client = http_client
        self._base_url = conf.cas_api_base_url
        self._auth = (conf.cas_api_username, conf.cas_api_password)
        self._headers = {"x-access-token": conf.cas_api_access_token, "x-cas-id": str(user.cas_id)}

    async def _request(
        self,
        *,
        method: Literal["GET", "POST", "DELETE"],
        path: str,
        data: Any = None,
    ) -> Any:
        """
        Выполняет запрос к сервису CAS.

        :param method: HTTP метод
        :param path: Путь
        :param data: Данные
        :return: Ответ от сервиса CAS
        """
        client_reponse = await self._client.request(
            method=method,
            url=get_full_url(self._base_url, path),
            json=data,
            auth=self._auth,
            headers=self._headers,
        )

        client_reponse.raise_for_status()
        response = client_reponse.json()

        if not isinstance(response, dict) or "success" not in response:
            raise ValueError("Неожиданный результат CAS клиента", response)

        # если запрос не успешен, то выбрасываем ошибку
        if not response["success"]:
            code, error = response.get("code"), response.get("error")
            raise (
                HTTPException(code, error)
                if code is not None and error is not None
                else ValueError("Неожиданный результат CAS клиента", response)
            )

        return response.get("data", None)

    async def get_user_by_phone(self, phone: str) -> CasUser:
        """
        Получает данные пользователя по телефону.

        :param phone: Телефон пользователя
        :return: Данные пользователя
        """
        CasClientUserDataValidation(phone=phone, cas_id=None)

        response = await self._request(
            method="GET",
            path=f"/rest/v1/srv/user?login={phone}",
        )

        # Проверяем что в ответе есть данные пользователя
        if not isinstance(response, dict):
            raise ValueError("Неожиданный результат CAS клиента", response)

        return CasUser.construct(
            cas_id=response["casId"],
            cas_roles=response["authorities"],
            phone=response["phone"],
            first_name=response["firstName"],
            middle_name=response["middleName"],
            last_name=response["lastName"],
        )

    async def get_users_by_cas_ids(self, cas_ids: list[int]) -> dict[int, CasUser]:
        """
        Получает данные пользователей по списку CAS идентификаторов.

        :param cas_ids: Список CAS идентификаторов пользователей
        :return: Словарь с данными пользователей
        """
        if not cas_ids:
            return {}

        response = await self._request(
            method="POST",
            path="/rest/srv/v2/users/info",
            data={"casIds": list(set(cas_ids))},
        )

        # Проверяем что в ответе есть данные пользователей
        if not isinstance(response, list):
            raise ValueError("Неожиданный результат CAS клиента", response)

        return {
            user_data["casId"]: CasUser.construct(
                cas_id=user_data["casId"],
                cas_roles=user_data["roles"],
                phone=user_data["phone"],
                first_name=user_data["firstName"],
                middle_name=user_data["middleName"],
                last_name=user_data["lastName"],
            )
            for user_data in response
        }

    async def add_role_by_cas_id(self, cas_id: int, role: str) -> None:
        """
        Добавляет роль редактора пользователю по CAS идентификатору.

        :param cas_id: идентификатор пользователя в CAS
        :param role: Роль
        """
        CasClientUserDataValidation(cas_id=cas_id, phone=None)

        try:
            await self._request(
                method="POST",
                path=f"/rest/v1/srv/users/{cas_id}/roles?role={role}",
            )

        except HTTPException as http_err:
            # Если роль уже назначена, то ничего не делаем
            if http_err.status_code == 409:
                return
            # Если пользователь не найден, то возвращаем 404
            elif http_err.status_code == 500 and "is not present in table" in http_err.detail:
                raise HTTPException(404, f"Пользователь с CAS идентификатором {cas_id} не найден") from http_err

            raise http_err

    async def delete_role_by_cas_id(self, cas_id: int, role: str) -> None:
        """
        Удаляет роль редактора у пользователя по CAS идентификатору.

        :param cas_id: идентификатор пользователя в CAS
        :param role: Роль
        """
        CasClientUserDataValidation(cas_id=cas_id, phone=None)

        await self._request(
            method="DELETE",
            path=f"/rest/v1/srv/users/{cas_id}/roles/{role}",
        )  # CAS не возвращает ошибку, если запрос корректный
