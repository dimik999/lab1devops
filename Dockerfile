# Сборка и запуск веб-приложения в контейнере
FROM python:3.11-slim

WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости (без тестовых для production-образа)
# Увеличенный таймаут и число повторов — при медленном канале до PyPI из контейнера
RUN pip install --no-cache-dir --timeout=120 --retries=10 flask==3.0.0

# Копируем код приложения
COPY app.py .

# Порт приложения
EXPOSE 5000

# Запуск приложения
CMD ["python", "app.py"]
