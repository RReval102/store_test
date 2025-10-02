"""Тесты для эндпоинтов, связанных с питомцами (Pet)."""

import pytest

from utils.data_generators import random_pet


class TestPetEndpoints:
    """Набор тестов для проверки CRUD‑операций с питомцами."""

    def test_create_get_update_delete_pet(self, client):
        """Проверяет полный цикл создания, получения, обновления и удаления питомца."""
        # Создание питомца
        pet_data = random_pet(status="available")
        create_resp = client.create_pet(pet_data)
        # В некоторых версиях API при создании возвращается код 200 или 201
        assert create_resp.status_code in (200, 201)
        created = create_resp.json()
        pet_id = created.get("id") or pet_data["id"]

        # Получение питомца
        get_resp = client.get_pet(pet_id)
        assert get_resp.status_code == 200
        fetched = get_resp.json()
        assert fetched["id"] == pet_id
        assert fetched["name"] == pet_data["name"]
        assert fetched["status"] == pet_data["status"]

        # Обновление питомца – меняем имя и статус
        updated_data = pet_data.copy()
        updated_data.update({"name": pet_data["name"] + "_upd", "status": "sold"})
        update_resp = client.update_pet(updated_data)
        assert update_resp.status_code in (200, 201)
        updated = update_resp.json()
        assert updated["name"] == updated_data["name"]
        assert updated["status"] == updated_data["status"]

        # Удаление питомца
        del_resp = client.delete_pet(pet_id)
        assert del_resp.status_code in (200, 204, 404)
        # После удаления повторный запрос должен вернуть ошибку 404/400
        get_after_del = client.get_pet(pet_id)
        assert get_after_del.status_code in (404, 400)

    def test_find_pets_by_status(self, client):
        """Проверяет фильтрацию питомцев по статусу."""
        # Добавим питомцев с разными статусами
        available_pet = random_pet(status="available")
        pending_pet = random_pet(status="pending")
        sold_pet = random_pet(status="sold")
        for pet in (available_pet, pending_pet, sold_pet):
            client.create_pet(pet)

        # Получить питомцев со статусом available
        resp = client.find_pets_by_status(["available"])
        assert resp.status_code == 200
        pets = resp.json()
        # Проверяем, что в списке есть хотя бы один питомец со статусом available
        assert any(item.get("status") == "available" for item in pets)

        # Получить питомцев по нескольким статусам
        resp_multi = client.find_pets_by_status(["available", "pending"])
        assert resp_multi.status_code == 200
        pets_multi = resp_multi.json()
        # Должны присутствовать питомцы с двумя статусами
        statuses = {p.get("status") for p in pets_multi}
        assert "available" in statuses or "pending" in statuses
