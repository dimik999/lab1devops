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
3. **deploy** — выполняется на **self-hosted runner** (например WSL на вашем ПК): локально вызываются `docker login`, `pull` и `run`. Облачный раннер не может подключиться по SSH к внутреннему IP WSL (`172.x`), поэтому деплой перенесён на вашу машину.

### Деплой только с WSL (без VPS)

1. В WSL установите **Docker** (или включите интеграцию **Docker Desktop** с этим дистрибутивом), проверьте: `docker ps`.
2. Зарегистрируйте **self-hosted runner** по инструкции GitHub: **Settings → Actions → Runners → New self-hosted runner** (Linux x64), папка в `~`, не в `system32`.
3. После `./config.sh` держите агент запущенным: `./run.sh` (пока окно открыто, runner в сети).
4. Пуш в `main`/`master`: job **deploy** пойдёт на ваш runner и поднимет контейнер на **порту 5000** в WSL. С Windows в браузере обычно: **http://localhost:5000** (если Docker Desktop пробрасывает порты).

Секреты **`SERVER_HOST` / `SERVER_USER` / `SERVER_SSH_KEY` / `SERVER_PORT` для текущего workflow не нужны** (они были для SSH-деплоя на удалённый сервер с **публичным** IP).

### Секреты (опционально)

Секреты `DOCKER_USERNAME` и `DOCKERHUB_TOKEN` в этом workflow **не используются**: образ публикуется в **ghcr.io** через `GITHUB_TOKEN`.

Если позже понадобится деплой по SSH на VPS — нужен **публичный** `SERVER_HOST` и отдельная настройка шага `appleboy/ssh-action` в workflow.

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
