"""Тесты для эндпоинтов, связанных с пользователями (User)."""

import pytest

from utils.data_generators import random_user


class TestUserEndpoints:
    """Проверка CRUD‑операций над пользователями."""

    def test_create_get_update_delete_user(self, client):
        """Проверяет создание, получение, обновление и удаление пользователя."""
        # Создаем пользователя
        user_data = random_user(password="P@ssw0rd123")
        create_resp = client.create_user(user_data)
        assert create_resp.status_code in (200, 201)
        username = user_data["username"]

        # Получаем пользователя
        get_resp = client.get_user(username)
        assert get_resp.status_code == 200
        fetched = get_resp.json()
        assert fetched["username"] == username
        assert fetched["email"] == user_data["email"]

        # Обновляем пользователя – меняем email и lastName
        updated_data = user_data.copy()
        updated_data.update({"email": "updated_" + user_data["email"], "lastName": "Smith"})
        update_resp = client.update_user(username, updated_data)
        assert update_resp.status_code in (200, 201)

        # Проверяем обновлённые данные
        get_after_update = client.get_user(username)
        assert get_after_update.status_code == 200
        updated_user = get_after_update.json()
        assert updated_user["email"] == updated_data["email"]
        assert updated_user["lastName"] == updated_data["lastName"]

        # Удаляем пользователя
        del_resp = client.delete_user(username)
        assert del_resp.status_code in (200, 204, 404)

        # Проверяем, что пользователя больше нет
        get_after_del = client.get_user(username)
        assert get_after_del.status_code in (404, 400)
