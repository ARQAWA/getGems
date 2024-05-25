# from datetime import (
#     datetime,
#     timedelta,
# )
# from typing import (
#     Annotated,
#     Iterable,
# )
# from zoneinfo import ZoneInfo
#
# from . import HttpClientManager
#
# __all__ = ("StorageClient",)
#
#
# class StorageClient(DependencyLayerBase):
#     """Клиент для работы со Storage."""
#
#     __depends__ = Annotated["StorageClient", None]
#
#     def __init__(
#         self,
#         user: User.__depends__,
#         http_client: HttpClientManager.__depends__,
#     ) -> None:
#         self._client = http_client
#         self._base_url = conf.storage_api_base_url
#         self._client_url = conf.storage_client_link_base_url
#         self._headers = {"x-access-token": conf.storage_api_access_token, "x-cas-id": str(user.cas_id)}
#
#     async def get_files_links(self, file_ids: Iterable[int]) -> dict[int, str]:
#         """
#         Получение ссылок на файлы хранилища на 3 часа.
#
#         :param file_ids: Идентификаторы файлов
#         :return: Словарь идентификаторов файлов и ссылок на них
#         """
#         expiration_date = (datetime.now() + timedelta(hours=3)).astimezone(ZoneInfo("UTC")).strftime("%Y-
#         %m-%dT%H:%M%z")
#         payload = [
#             {
#                 "fileId": file_id,
#                 "grants": ["FILE_READ", "META_READ"],
#                 "grantType": "NO_RESTRICTION",
#                 "exp": expiration_date,
#             }
#             for file_id in file_ids
#         ]
#
#         if not payload:
#             return {}
#
#         client_reponse = await self._client.request(
#             method="POST",
#             url=get_full_url(self._base_url, "/srv/v1/files/links"),
#             json=payload,
#             headers=self._headers,
#         )
#
#         client_reponse.raise_for_status()
#         response = client_reponse.json()
#
#         if not isinstance(response, dict) or "data" not in response or not isinstance(response["data"], list):
#             raise ValueError("Неожиданный ответ от сервиса Storage", response)
#
#         try:
#             return {
#                 file_result["fileId"]: self._client_url + file_result["fileLink"]
#                 for file_result in response["data"]
#                 if file_result["result"] == "PERMITTED"
#             }
#         except Exception as exc:
#             raise ValueError("Неожиданный ответ от сервиса Storage", response) from exc
