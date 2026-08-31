# 🚀 Getting Started - Dashboardku

Quick commands untuk mulai development.

## ⚡ Quick Start (Docker)

```bash
# 1. Build dan start containers
docker compose up --build -d

# 2. Run migrations pertama kali
docker compose exec dashboardku alembic upgrade head

# 3. Buka browser ke http://localhost:8000/docs
```

## 💻 Local Development

```bash
# 1. Setup environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env sesuai kebutuhan lokal Anda

# 4. Run migrations
alembic upgrade head

# 5. Start server
make dev
```

## 🔧 Common Commands

| Command | Description |
|---------|-------------|
| `make help` | Lihat semua command yang tersedia |
| `make dev` | Start development server (local) |
| `make docker-up` | Start containers via Docker Compose |
| `make migrate-up` | Apply database migrations |
| `make shell` | Enter application shell |
| `make mysql-shell` | Enter MySQL CLI shell |
| `make log` | View container logs |

## 🌐 Access Points

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API Health**: http://localhost:8000/health

## 🔒 First-Time Setup

1. Create `.env` file:
```bash
cp .env.example .env
```

2. Edit important values:
- `APP_USERNAME` & `APP_PASSWORD` → your credentials
- `SECRET_KEY` → random string (use `openssl rand -hex 32`)

## 📝 Testing API Calls

### Health Check
```bash
curl http://localhost:8000/health
```

### Login (after auth implemented)
```bash
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "changeme"}'
```

## 🛠️ Troubleshooting

### Database Connection Error
```bash
# Ensure MySQL is running
docker compose ps

# Restart MySQL only
docker compose restart mysql
```

### Port Already in Use
```bash
# Change port in docker-compose.yml or modify .env
# Default: 8000 for app, 3306 for MySQL
```

### Migration Failed
```bash
# Reset database (⚠️ DELETES ALL DATA)
docker compose down && docker volume rm dashboardku_mysql_data
docker compose up -d
docker compose exec dashboardku alembic upgrade head
```

## ✅ Verification Checklist

- [x] Containers running (`docker compose ps`)
- [x] Database accessible (`docker compose exec mysql mysql -psecret dashboardku`)
- [x] API responding (`curl http://localhost:8000/health`)
- [x] Migrations applied (`SELECT * FROM projects;` returns empty but no error)

---

Next step: Follow [docs/PHASE_1_SUMMARY.md](./docs/PHASE_1_SUMMARY.md) for detailed architecture info.
