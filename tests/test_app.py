"""Тесты для веб-приложения."""
import pytest
from app import app


@pytest.fixture
def client():
    """Клиент для тестирования."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    """Проверка главной страницы."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Лабораторная работа".encode("utf-8") in response.data


def test_health(client):
    """Проверка эндпоинта health."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
