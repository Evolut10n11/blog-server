Blog Server

Минимальный блог‑сервер на FastAPI, запускаемый в Docker‑контейнере с базой PostgreSQL и автоматическим деплоем через GitHub Actions.

Структура проекта

.
├── app/                  # Исходники приложения
│   └── main.py           # FastAPI-приложение
├── logs/                 # Точка монтирования для логов
├── Dockerfile            # Образ приложения
├── docker-compose.yml    # Описание сервисов Docker Compose
└── README.md             # Инструкция по проекту

Требования

Docker (Desktop или Engine с поддержкой Compose)

Docker Compose

Git

(опционально для локальной dev) Python 3.11 и зависимости из requirements.txt

Локальный запуск

Через Docker

cd blog-server
docker compose up --build -d

Контейнеры доступны по адресу http://localhost:8080

Логи приложения в logs/app, логи БД в logs/db

Локальная разработка без Docker

python -m venv .venv
. .venv/Scripts/Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

API

GET /posts

Возвращает список публикаций.
curl http://localhost:8080/posts

Response:
[]

POST /posts
curl -X POST http://localhost:8080/posts \
  -H "Content-Type: application/json" \
  -d '{"title":"Hello","content":"World"}'
Response:
{"id":1,"title":"Hello","content":"World"}

Список технологий

Python 3.11

FastAPI, Uvicorn

SQLAlchemy, Databases

PostgreSQL

Docker, Docker Compose

GitHub Actions (CI/CD)

Smoke‑тест

curl GET /posts → []

curl POST /posts → возвращает созданный объект

curl GET /posts → публикация в списке

CI/CD (GitHub Actions)

При пуше в ветку main запускается workflow .github/workflows/deploy.yml, который на self‑hosted runner:

Проверяет код (actions/checkout@v3).

Выполняет:
docker compose down || true
docker compose up -d --build

Для работы CI нужен self-hosted runner:

Settings → Actions → Runners → New self-hosted runner (Windows) → установка и запуск как службы.

Runner должен иметь права на запуск Docker

Автор: Иван Rodionov