# Dashboardku 🚀

Personal Task Management System dengan Webhook Notification (WAHA) & MySQL.

## ⚡ Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+

### Development Setup

#### Option 1: Using Docker (Recommended)

```bash
# Build dan start containers
docker compose up --build -d

# Run database migrations
docker compose exec dashboardku alembic upgrade head

# View logs
docker compose logs -f dashboardku
```

Aplikasi akan berjalan di `http://localhost:8000`
Swagger UI tersedia di `http://localhost:8000/docs`

#### Option 2: Local Development

```bash
# Setup virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup .env file
cp .env.example .env
# Edit .env sesuai konfigurasi lokal Anda

# Run migrations
alembic upgrade head

# Start development server
make dev
```

## 📁 Project Structure

```
dashboardku/
├── app/                    # Application codebase
│   ├── api/               # REST API endpoints
│   │   └── routes/        # Route modules
│   ├── services/          # Business logic
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   ├── main.py           # FastAPI entry point
│   └── config.py         # Configuration settings
├── alembic/              # Database migrations
├── docker-compose.yml    # Container orchestration
├── Dockerfile           # App container image
└── Makefile             # Utility commands
```

## 🔧 Makefile Commands

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make dev` | Run development server locally |
| `make migrate-up` | Apply pending migrations |
| `make docker-build` | Build Docker images |
| `make docker-up` | Start Docker containers |
| `make docker-down` | Stop Docker containers |
| `make shell` | Enter application shell |
| `make mysql-shell` | Enter MySQL shell |
| `make log` | View application logs |

## 🗄️ Database Schema

### Projects
- id, name, color, icon, status, created_at

### Tasks
- id, project_id, title, description, priority, status, deadline, completed_at

### Reminders
- id, task_id, reminder_type, relative_value, relative_unit, absolute_time, sent

### Webhook Configs
- id, name, endpoint_url, headers, message_template, is_active

### Notification Logs
- id, task_id, reminder_id, webhook_config_id, status, response_code, retry_count

## 🔐 Environment Variables

Create `.env` from `.env.example`:

```bash
cp .env.example .env
```

Required variables:
- `DB_HOST`, `DB_USER`, `DB_PASS`, `DB_NAME` - MySQL connection
- `APP_USERNAME`, `APP_PASSWORD` - Authentication credentials
- `SECRET_KEY` - Session signing key (change in production!)
- `WAHA_WEBHOOK_URL` - WhatsApp Gateway endpoint

## 🌐 API Documentation

After starting the server:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Endpoints:
- `POST /api/login` - Authentication
- `GET/POST /api/projects` - Project management
- `GET/POST /api/tasks` - Task CRUD operations
- `GET/POST /api/reminders` - Reminder configuration
- `GET/PUT /api/webhook/config` - Webhook settings

## 📦 Tech Stack

- **Backend**: FastAPI + SQLAlchemy + Alembic
- **Database**: MySQL 8.0
- **Scheduler**: APScheduler
- **Deployment**: Docker & Docker Compose

## 🛠️ Development Workflow

### Create New Migration

```bash
# From project root
make migrate-revision MESSAGE="Describe your migration"
# or directly:
alembic revision --autogenerate -m "message"
```

### Run Tests

```bash
# Local test runner
make test
```

### Reset Database

```bash
# Drop and recreate all tables
make migrate-clean  # TODO: implement this command
```

## 🤝 Contributing

This is a personal project, but feel free to fork and modify for your needs!

## 📝 License

MIT License - See LICENSE file for details

---

**Status**: Phase 1 ✅ Foundation
Phase 2 ✅ Core CRUD  
Phase 3 ✅ Notification System
Phase 4 ✅ Frontend Implementation

**Next**: Phase 5 Testing & Deployment 🚀

