"""Тесты для эндпоинтов, связанных с магазином (Store)."""

import pytest

from utils.data_generators import random_order, random_pet


class TestStoreEndpoints:
    """Проверка заказов и инвентаризации в Store."""

    def test_place_get_delete_order(self, client):
        """Проверяет создание, получение и удаление заказа."""
        # Сначала создадим питомца, чтобы гарантировать корректный petId
        pet = random_pet(status="available")
        client.create_pet(pet)
        pet_id = pet["id"]

        # Создаем заказ
        order_data = random_order(pet_id=pet_id, quantity=2, status="placed")
        order_resp = client.place_order(order_data)
        assert order_resp.status_code in (200, 201)
        order = order_resp.json()
        order_id = order.get("id") or order_data["id"]

        # Получаем заказ
        get_resp = client.get_order(order_id)
        assert get_resp.status_code == 200
        fetched = get_resp.json()
        assert fetched["id"] == order_id
        assert fetched["petId"] == pet_id

        # Удаляем заказ
        del_resp = client.delete_order(order_id)
        assert del_resp.status_code in (200, 204, 404)

        # После удаления заказ должен отсутствовать
        get_after_del = client.get_order(order_id)
        assert get_after_del.status_code in (404, 400)

    def test_inventory_returns_map(self, client):
        """Проверяет, что инвентарь возвращает словарь со статусами."""
        resp = client.get_inventory()
        assert resp.status_code == 200
        inventory = resp.json()
        assert isinstance(inventory, dict)
        # Значения должны быть числами (количество питомцев)
        for value in inventory.values():
            assert isinstance(value, int)
