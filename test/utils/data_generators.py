"""Генераторы случайных данных для тестов.


"""

from __future__ import annotations

import random
import string
import time
from typing import Any, Dict, List, Optional


def _random_id() -> int:
    """Возвращает псевдослучайный идентификатор на основе текущего времени."""
    ts_part = int(time.time() * 1000) % 1_000_000  # последние 6 цифр ms
    rand_part = random.randint(0, 999_999)
    return ts_part * 1_000_000 + rand_part


def random_pet(
    name: Optional[str] = None,
    status: str = "available",
    photo_urls: Optional[List[str]] = None,
    category: Optional[Dict[str, Any]] = None,
    tags: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Создаёт словарь с данными нового питомца"""
    if name is None:
        name = "pet_" + "".join(random.choices(string.ascii_lowercase, k=8))
    if photo_urls is None:
        photo_urls = ["https://example.com/photo.jpg"]
    if category is None:
        category = {"id": random.randint(1, 1000), "name": "category"}
    if tags is None:
        tags = []
    return {
        "id": _random_id(),
        "category": category,
        "name": name,
        "photoUrls": photo_urls,
        "tags": tags,
        "status": status,
    }


def random_order(
    pet_id: Optional[int] = None,
    quantity: int = 1,
    status: str = "placed",
    complete: bool = False,
) -> Dict[str, Any]:
    """Создаёт словарь с данными для заказа."""
    if pet_id is None:
        pet_id = _random_id()
    return {
        "id": random.randint(1, 10),  # используем диапазон 1-10 для успешного ответа【434211662711270†L87-L95】
        "petId": pet_id,
        "quantity": quantity,
        "shipDate": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),
        "status": status,
        "complete": complete,
    }


def random_user(
    username: Optional[str] = None,
    first_name: str = "John",
    last_name: str = "Doe",
    email: Optional[str] = None,
    password: str = "pass123",
    phone: str = "+1234567890",
    user_status: int = 0,
) -> Dict[str, Any]:
    """Создаёт словарь с данными для пользователя."""
    if username is None:
        username = "user_" + "".join(random.choices(string.ascii_lowercase, k=8))
    if email is None:
        email = f"{username}@example.com"
    return {
        "id": _random_id(),
        "username": username,
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "password": password,
        "phone": phone,
        "userStatus": user_status,
    }