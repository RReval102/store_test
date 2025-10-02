"""Тесты для проверки входа и выхода пользователя."""

import pytest

from utils.data_generators import random_user


class TestLoginLogout:
    def test_login_logout_user(self, client):
        """Создаёт пользователя, выполняет вход и выход из системы."""
        # Создаём нового пользователя с известным паролем
        password = "TestPass123!"
        user_data = random_user(password=password)
        client.create_user(user_data)
        username = user_data["username"]

        # Вход в систему
        login_resp = client.login_user(username, password)
        # При успешном входе возвращается код 200 и строка с сессией【434211662711270†L129-L138】
        assert login_resp.status_code == 200
        assert isinstance(login_resp.text, str)
        assert "logged in user session" in login_resp.text.lower()

        # Выход из системы
        logout_resp = client.logout_user()
        # Успешный выход возвращает код 200【434211662711270†L139-L143】
        assert logout_resp.status_code == 200
