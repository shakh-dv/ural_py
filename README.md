# Ural Back на Python/FastAPI

Этот каталог содержит backend на Python/FastAPI, исключительно в ознокомительных целях.

## Структура

- `app/routes` — HTTP роуты по модулям (`auth`, `users`, `tasks`, и т.д.)
- `app/services` — сервисный слой с бизнес-логикой
- `app/models.py` — SQLAlchemy-модели
- `app/schemas.py` — Pydantic-схемы
- `app/main.py` — инициализация приложения и подключение роутов
- `docker-compose.yml` — self-hosted деплой со связкой Traefik + Nginx + FastAPI

## Локальный запуск (без Docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 4000
```

## Self-hosted деплой в Docker

### 1) Подготовка переменных окружения

```bash
cp .env.example .env
```

Заполните:

- `APP_DOMAIN` — домен API (например, `api.example.com`)
- `LETSENCRYPT_EMAIL` — email для ACME/Let's Encrypt
- `DATABASE_URL` — строка подключения к PostgreSQL

### 2) Запуск

```bash
docker compose up -d --build
```

Что поднимается:

- `traefik` — edge proxy, HTTPS и автополучение сертификатов Let's Encrypt
- `nginx` — внутренний reverse proxy и отдача статики `/uploads/dispatch`
- `app` — FastAPI приложение

### 3) Обновление после изменений

```bash
docker compose up -d --build app nginx
```

## Модули API

- auth
- users
- tasks
- user-tasks
- referrals
- levels и level-config
- taps
- boost-items и boost-effects
- raffles
- telegram
- uploads

## Environment

- `DATABASE_URL` (PostgreSQL)
- `UPLOAD_DIR` (необязательно, папка для upload-файлов)
- `TELEGRAM_BOT_TOKEN` (обязательно, токен бота для валидации Telegram Login)
