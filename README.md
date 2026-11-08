# Task Tracker

Учебный трекер задач: FastAPI REST API, веб-интерфейс, in-memory или PostgreSQL.

## Возможности

- Создание задачи, список, отметка выполнения
- Поля задачи: `id`, `title`, `completed`, `created_at`
- Переключение хранилища: `STORAGE_BACKEND=memory|postgres`

## API

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/health` | Проверка живости |
| POST | `/api/tasks` | `{ "title": "..." }` |
| GET | `/api/tasks` | Список задач |
| PATCH | `/api/tasks/{id}` | `{ "completed": true }` |

Документация OpenAPI: `http://127.0.0.1:8000/docs` (если статика не перехватывает — остановите mount или используйте порт без фронта).

## Локальный запуск (in-memory)

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
set STORAGE_BACKEND=memory
uvicorn app.main:app --reload
```

Откройте `http://127.0.0.1:8000/`.

## PostgreSQL (Docker)

```bash
docker compose up -d db
copy .env.example .env
# В .env: STORAGE_BACKEND=postgres и DATABASE_URL=postgresql+psycopg2://tasktracker:tasktracker@localhost:5433/tasktracker
# (порт 5433, если 5432 уже занят другим PostgreSQL)
uvicorn app.main:app --reload
```

## Тесты

```bash
set STORAGE_BACKEND=memory
pytest -q
```

## Продакшн (VPS + Docker Compose)

На сервере с Docker:

```bash
git clone <your-repo-url> task-tracker
cd task-tracker
# Создайте .env.prod с POSTGRES_PASSWORD=...
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d --build
```

Проверка: `curl http://your-server/health` → `{"status":"ok"}`.

TLS: перед `nginx` добавьте reverse proxy с Let's Encrypt (certbot) или расширьте `nginx.conf` для 443.

## Структура

- `app/` — FastAPI, репозитории, модели БД
- `frontend/` — статический UI
- `tests/` — pytest
