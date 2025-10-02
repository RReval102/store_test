"""Простой клиент для взаимодействия с API Swagger Petstore.

Использование данного клиента позволяет централизовать формирование
URL, обработку кодов ответов и легко переопределять базовый URL при
необходимости.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Iterable, List, Optional

import requests


class PetStoreClient:

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def _url(self, path: str) -> str:
        """Формирует абсолютный URL для переданного относительного пути."""
        return f"{self.base_url}{path}" if path.startswith("/") else f"{self.base_url}/{path}"

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Any] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_statuses: Iterable[int] | None = None,
    ) -> requests.Response:
        """Выполняет HTTP‑запрос и возвращает ответ.

        :param method: HTTP‑метод (GET, POST, PUT, DELETE)
        :param path: относительный путь к ресурсу
        :param params: параметры запроса (query)
        :param json_data: тело запроса в формате JSON
        :param data: тело запроса в формате form data
        :param files: файлы для отправки (используется для uploadImage)
        :param headers: дополнительные заголовки
        :param expected_statuses: список допустимых кодов ответа. 
        :return: объект ``requests.Response``
        """
        url = self._url(path)
        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=json_data,
            data=data,
            files=files,
            headers=headers,
        )
        
        if expected_statuses is not None and response.status_code not in expected_statuses:
            raise AssertionError(
                f"Unexpected status code {response.status_code} for {method} {url}; "
                f"expected one of {expected_statuses}"
            )
        return response

    
    def create_pet(self, pet_data: Dict[str, Any]) -> requests.Response:
        """Создает нового питомца (POST /pet)."""
        return self._request(
            method="POST",
            path="/pet",
            json_data=pet_data,
            expected_statuses=[200, 201],
        )

    def update_pet(self, pet_data: Dict[str, Any]) -> requests.Response:
        
        return self._request(
            method="PUT",
            path="/pet",
            json_data=pet_data,
            expected_statuses=[200, 201, 400, 404],
        )

    def get_pet(self, pet_id: int) -> requests.Response:
        
        return self._request(
            method="GET",
            path=f"/pet/{pet_id}",
            expected_statuses=[200, 400, 404],
        )

    def delete_pet(self, pet_id: int, api_key: Optional[str] = None) -> requests.Response:
        
        headers = {"api_key": api_key} if api_key else None
        return self._request(
            method="DELETE",
            path=f"/pet/{pet_id}",
            headers=headers,
            expected_statuses=[200, 400, 404],
        )

    def find_pets_by_status(self, statuses: List[str]) -> requests.Response:
        """Находит питомцев по статусу (GET /pet/findByStatus).

        Параметр ``statuses`` должен быть списком строк. Значения могут быть
        ``"available"``, ``"pending"`` или ``"sold"`` согласно
        спецификации【434211662711270†L35-L42】.
        """
        params: Dict[str, Any] = {}
        # API использует формат collectionFormat=multi, поэтому передаём
        
        params["status"] = statuses
        return self._request(
            method="GET",
            path="/pet/findByStatus",
            params=params,
            expected_statuses=[200, 400],
        )

    
    def get_inventory(self) -> requests.Response:
        
        return self._request(
            method="GET",
            path="/store/inventory",
            expected_statuses=[200],
        )

    def place_order(self, order_data: Dict[str, Any]) -> requests.Response:
        """Создаёт заказ (POST /store/order)."""
        return self._request(
            method="POST",
            path="/store/order",
            json_data=order_data,
            expected_statuses=[200, 400],
        )

    def get_order(self, order_id: int) -> requests.Response:
        """Получает заказ по идентификатору (GET /store/order/{orderId})."""
        return self._request(
            method="GET",
            path=f"/store/order/{order_id}",
            expected_statuses=[200, 400, 404],
        )

    def delete_order(self, order_id: int) -> requests.Response:
        """Удаляет заказ по идентификатору (DELETE /store/order/{orderId})."""
        return self._request(
            method="DELETE",
            path=f"/store/order/{order_id}",
            expected_statuses=[200, 400, 404],
        )

    
    def create_user(self, user_data: Dict[str, Any]) -> requests.Response:
        """Создаёт пользователя (POST /user)."""
        return self._request(
            method="POST",
            path="/user",
            json_data=user_data,
            expected_statuses=[200, 201],
        )

    def get_user(self, username: str) -> requests.Response:
        """Получает пользователя по имени (GET /user/{username})."""
        return self._request(
            method="GET",
            path=f"/user/{username}",
            expected_statuses=[200, 400, 404],
        )

    def update_user(self, username: str, user_data: Dict[str, Any]) -> requests.Response:
        """Обновляет данные пользователя (PUT /user/{username})."""
        return self._request(
            method="PUT",
            path=f"/user/{username}",
            json_data=user_data,
            expected_statuses=[200, 400, 404],
        )

    def delete_user(self, username: str) -> requests.Response:
        """Удаляет пользователя (DELETE /user/{username})."""
        return self._request(
            method="DELETE",
            path=f"/user/{username}",
            expected_statuses=[200, 400, 404],
        )

    def login_user(self, username: str, password: str) -> requests.Response:
        
        params = {"username": username, "password": password}
        return self._request(
            method="GET",
            path="/user/login",
            params=params,
            expected_statuses=[200, 400],
        )

    def logout_user(self) -> requests.Response:
        
        return self._request(
            method="GET",
            path="/user/logout",
            expected_statuses=[200],
        )
