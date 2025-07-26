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
└── README.md              # Инструкция по проекту
```

---

## Требования

- Docker (Desktop или Engine + Compose)  
- Docker Compose  
- Git  
- *(опционально)* Python 3.11 и зависимости из `requirements.txt` для локальной разработки без Docker

---

## Локальный запуск


### 1. Запуск через Docker Compose

```bash
cd blog-server
docker compose up --build -d
```

- Приложение доступно: `http://localhost:8080`  
- Логи приложения — `logs/app`  
- Логи PostgreSQL — `logs/db`

---

## API

### GET /posts

Возвращает список публикаций.

```bash
curl http://localhost:8080/posts
```

**Response (200 OK)**

```json
[]
```

### POST /posts

Добавляет новую публикацию.

```bash
curl -X POST http://localhost:8080/posts   -H "Content-Type: application/json"   -d '{"title":"Another post","content":"Some content here"}'
```

**Response (200 OK)**

```json
{"id":1,"title":"Another post","content":"Some content here"}
```

---

## Smoke-тест

1. **GET /posts** (ожидается пустой список):
   ```bash
   curl http://localhost:8080/posts
   ```
2. **POST /posts** (добавить публикацию):
   ```powershell
   Invoke-RestMethod `
     -Uri http://localhost:8080/posts `
     -Method POST `
     -ContentType 'application/json' `
     -Body '{"title":"Test","content":"Hello"}'
   ```
3. **GET /posts** (должен показать созданную запись):
   ```bash
   curl http://localhost:8080/posts
   ```

---

## Остановка и запуск

**Остановка контейнеров**  
```powershell
cd blog-server
docker compose down
```

**Повторный запуск**  
```powershell
cd blog-server
docker compose up --build -d
```

---

## CI/CD (GitHub Actions)

**Примечание:** При использовании self-hosted runner не требуются SSH-секреты (`SSH_PRIVATE_KEY`, `SERVER_HOST`, `SERVER_USER`).

При пуше в ветку `main` запускается workflow:

```yaml
name: Local Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: self-hosted

    steps:
      - uses: actions/checkout@v3

      - name: Build & Restart Containers
        shell: powershell
        run: |
          cd $Env:GITHUB_WORKSPACE
          docker compose down
          docker compose up -d --build
```

### Установка self-hosted runner (Windows)

```powershell
# Create a folder under the drive root
$ mkdir actions-runner; cd actions-runner# Download the latest runner package
$ Invoke-WebRequest -Uri https://github.com/actions/runner/releases/download/v2.326.0/actions-runner-win-x64-2.326.0.zip -OutFile actions-runner-win-x64-2.326.0.zip# Optional: Validate the hash
$ if((Get-FileHash -Path actions-runner-win-x64-2.326.0.zip -Algorithm SHA256).Hash.ToUpper() -ne '539d48815f8ecda6903755025d5b578f919a32692b731d85a9a24419fe4dbd9e'.ToUpper()){ throw 'Computed checksum did not match' }# Extract the installer
$ Add-Type -AssemblyName System.IO.Compression.FileSystem ; [System.IO.Compression.ZipFile]::ExtractToDirectory("$PWD/actions-runner-win-x64-2.326.0.zip", "$PWD")
# Create the runner and start the configuration experience
$ ./config.cmd --url https://github.com/Evolut10n11/blog-server --token AOEE763BWKF7ZXG6DRAWUG3IQQZQO# Run it!
$ ./run.cmd
```

_Автор: Иван Rodionov_
