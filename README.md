# Лабораторная работа №1. Автоматизация развёртывания

Простое веб-приложение на Flask с Docker и CI/CD (GitHub Actions).

## Локальный запуск

```bash
pip install -r requirements.txt
python app.py
```

Приложение доступно по адресу http://localhost:5000

## Тесты

```bash
pytest tests/ -v
```

## Docker

Сборка образа:

```bash
docker build -t lab1-app .
docker run -p 5000:5000 lab1-app
```

## CI/CD (GitHub Actions)

При пуше в ветку `main` или `master` пайплайн:

1. **test** — запускает тесты (pytest)
2. **build-and-push** — собирает Docker-образ и публикует в GitHub Container Registry (ghcr.io)
3. **deploy** — деплоит на сервер по SSH (останавливает старый контейнер, подтягивает новый образ, запускает контейнер)

### Секреты в GitHub

В настройках репозитория (Settings → Secrets and variables → Actions) добавьте:

| Секрет | Описание |
|--------|----------|
| `DEPLOY_HOST` | IP или hostname сервера |
| `DEPLOY_USER` | Пользователь SSH на сервере |
| `DEPLOY_SSH_KEY` | Приватный SSH-ключ для доступа к серверу |

Для подтягивания образа с ghcr.io на сервере можно использовать тот же `GITHUB_TOKEN` или создать Personal Access Token с правом `read:packages` и передать его в deploy-скрипт (при необходимости настройте переменную `GHCR_TOKEN` в секретах).

## Деплой через Ansible

Установите зависимости:

```bash
pip install ansible ansible-core
# для модулей Docker:
ansible-galaxy collection install community.docker
```

Отредактируйте `ansible/inventory.yml` (IP сервера, имя образа). Запуск:

```bash
cd ansible
ansible-playbook -i inventory.yml playbook.yml
```

Для доступа к ghcr.io с сервера предварительно выполните на нём:

```bash
echo YOUR_GITHUB_PAT | docker login ghcr.io -u YOUR_USERNAME --password-stdin
```
