# Blog Server

Минимальный блог-сервер на FastAPI, Docker Compose и PostgreSQL с автоматическим деплоем через GitHub Actions (self-hosted runner).

---

## Структура проекта

```
.
├── app/                  # Исходники приложения
│   └── main.py           # FastAPI-приложение
├── logs/                 # Каталог для логов 
│   ├── app/              # Логи приложения 
│   └── db/               # Логи БД 
├── Dockerfile            # Описание сборки образа приложения
├── docker-compose.yml    # Описание сервисов Docker Compose
└── README.md             # Инструкция по проекту
```

---

## Требования

- **Docker** (Desktop или Docker Engine + Compose)  
- **Docker Compose**  
- **Git**  
- *(опционально)* Python 3.11 и зависимости из `requirements.txt` для локальной разработки без Docker

---

## Локальный запуск


### 1. Запуск через Docker Compose

```bash
cd blog-server
docker compose up --build -d
```

- Приложение доступно по адресу: `http://localhost:8080`  
- Логи приложения пишутся в папку `logs/app`  
- Логи PostgreSQL пишутся в папку `logs/db`

### 2. Локальная разработка без Docker

```bash
cd blog-server
python -m venv .venv
. .venv/Scripts/Activate.ps1   # PowerShell
# или: source .venv/bin/activate   # bash/zsh
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

---

## API

### GET /posts

Возвращает список всех публикаций.

```bash
curl http://localhost:8080/posts
```

**Response (200 OK)**

```json
[
  { "id": 1, "title": "Hello world", "content": "My first post!" }
]
```

---

### POST /posts

Добавляет новую публикацию.

**Request**

```bash
curl -X POST http://localhost:8080/posts \
  -H "Content-Type: application/json" \
  -d '{"title":"Another post","content":"Some content here"}'
```

**Response (200 OK)**

```json
{ "id": 2, "title": "Another post", "content": "Some content here" }
```

---

## Список технологий

- Python 3.11, FastAPI, Uvicorn  
- SQLAlchemy, Databases  
- PostgreSQL  
- Docker, Docker Compose  
- GitHub Actions с self-hosted runner на Windows  

---

## Smoke-тест

1. `curl GET /posts` → `[]`  
2. `curl POST /posts` → создаёт и возвращает новую запись  
3. `curl GET /posts` → публикация должна быть в списке  

---

## CI/CD (GitHub Actions)

При пуше в ветку `main` запускается workflow `.github/workflows/deploy.yml`:

```yaml
name: Local Deploy

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: self-hosted

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Build and restart containers
        shell: powershell
        run: |
```

### Установка self-hosted runner (Windows)

```powershell
Create a folder under the drive root

mkdir actions-runner; cd actions-runner
Download the latest runner package

Invoke-WebRequest -Uri https://github.com/actions/runner/releases/download/v2.326.0/actions-runner-win-x64-2.326.0.zip -OutFile actions-runner-win-x64-2.326.0.zip
Extract the installer
Add-Type -AssemblyName System.IO.Compression.FileSystem ; [System.IO.Compression.ZipFile]::ExtractToDirectory("$PWD/actions-runner-win-x64-2.326.0.zip", "$PWD")
Create the runner and start the configuration experience
./config.cmd --url https://github.com/Evolut10n11/blog-server --token ВАШ_ТОКЕН_НА_ГИТ
Run it!
./run.cmd
```

_Автор: Иван Rodionov_



