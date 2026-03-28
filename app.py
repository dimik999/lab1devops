"""Простое веб-приложение на Flask."""
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    """Главная страница."""
    return "<h1>Лабораторная работа №1. Автоматизация</h1><p>Веб-приложение успешно развёрнуто.</p>"


@app.route("/health")
def health():
    """Эндпоинт для проверки работоспособности."""
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
