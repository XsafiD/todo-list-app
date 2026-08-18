# Dashboardku 🚀

Personal Task Management System dengan notifikasi webhook (WAHA/WhatsApp) — pengganti Todoist yang bisa dikustomisasi penuh.

![Status](https://img.shields.io/badge/status-production--ready-brightgreen) ![Phases](https://img.shields.io/badge/phases-5%2F5%20complete-blue) ![License](https://img.shields.io/badge/license-MIT-lightgrey)

## ✨ Fitur

- **Task Management** — CRUD task dengan priority, status, deadline, dan auto-completion timestamp
- **Project Organization** — project berwarna dengan soft-delete (archive)
- **Flexible Reminders** — 3 tipe reminder:
  - `day_h` — otomatis notify di hari deadline (auto-created)
  - `relative` — X menit/jam/hari sebelum deadline
  - `absolute` — di tanggal & jam spesifik
- **Webhook Notifications** — POST ke WAHA/endpoint apapun dengan custom headers & template
- **Retry Mechanism** — exponential backoff untuk pengiriman gagal
- **Notification Logs** — audit trail semua notifikasi (status, response code, retry count)
- **Single-User Auth** — bcrypt password + HMAC-signed token (Basic/Bearer/X-API-Key)
- **Background Scheduler** — APScheduler cek deadline tiap menit tanpa blocking API

## 🛠️ Tech Stack

| Layer | Teknologi |
|-------|-----------|
| Backend | FastAPI (Python 3.11+), SQLAlchemy 2.0, Alembic |
| Database | MySQL 8.0 (Docker) |
| Scheduler | APScheduler (AsyncIO) |
| Frontend | Vanilla HTML + Alpine.js 3 + Tailwind CSS |
| Deployment | Docker Compose |

## ⚡ Quick Start

### Docker (Recommended)

```bash
# 1. Build & start
docker compose up --build -d

# 2. Jalankan migrasi database
docker compose exec dashboardku alembic upgrade head

# 3. Akses aplikasi
open http://localhost:8000        # Frontend
open http://localhost:8000/docs   # Swagger UI
```

### Local Development

```bash
# Setup environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Konfigurasi
cp .env.example .env    # edit DB_HOST=localhost untuk local

# Start MySQL saja via Docker
docker compose up -d mysql

# Migrasi & jalankan server
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

**Default login**: `admin` / `changeme` — **ganti di `.env` sebelum production!**

## 📁 Project Structure

```
dashboardku/
├── app/
│   ├── main.py                  # FastAPI entry point + scheduler lifecycle
│   ├── config.py                # Pydantic settings (.env)
│   ├── database.py              # SQLAlchemy engine & session
│   ├── models.py                # 5 ORM models
│   ├── schemas.py               # Pydantic request/response schemas
│   ├── security.py              # bcrypt + HMAC token
│   ├── api/
│   │   ├── dependencies.py      # require_auth (Basic/Bearer/API-Key)
│   │   └── routes/              # auth, projects, tasks, reminders, webhooks, stats
│   ├── services/
│   │   ├── scheduler.py         # APScheduler + reminder checker
│   │   ├── webhook.py           # HTTP POST + exponential backoff retry
│   │   └── notification.py      # Template engine
│   └── static/
│       ├── index.html           # SPA (login + dashboard + modals)
│       ├── css/style.css        # Design system (DESIGN.md)
│       └── js/app.js
├── alembic/                     # Migrations
├── docs/                        # Phase summaries, testing guide
├── docker-compose.yml
├── Dockerfile
├── Makefile
└── requirements.txt
```

## 🌐 API Endpoints

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| POST | `/api/login` | Dapatkan bearer token |
| GET | `/api/me` | Info user aktif |
| GET/POST | `/api/projects` | List / buat project |
| GET/PUT/DELETE | `/api/projects/{id}` | Detail / update / hapus |
| PATCH | `/api/projects/{id}/archive` | Archive/unarchive |
| GET | `/api/tasks` | List semua task (+filter status/project) |
| GET/POST | `/api/projects/{id}/tasks` | Task per project |
| GET/PUT/DELETE | `/api/tasks/{id}` | Detail / update / hapus |
| PATCH | `/api/tasks/{id}/complete` | Toggle completion |
| GET/POST | `/api/tasks/{id}/reminders` | Reminder per task |
| PUT/DELETE | `/api/reminders/{id}` | Update / hapus reminder |
| GET/POST | `/api/webhook/config` | Konfigurasi webhook |
| GET | `/api/webhook/test` | Kirim test notification |
| GET | `/api/notifications/logs` | Log notifikasi (+filter) |
| GET | `/api/stats` | Statistik dashboard |
| GET | `/health` | Health check |
| GET | `/scheduler/status` | Status scheduler |

Dokumentasi interaktif lengkap: **http://localhost:8000/docs**

## 🔧 Makefile Commands

| Command | Deskripsi |
|---------|-----------|
| `make dev` | Jalankan dev server lokal |
| `make docker-up` / `docker-down` | Start/stop containers |
| `make migrate-up` | Apply migrations |
| `make migrate-revision MESSAGE="..."` | Buat migration baru |
| `make mysql-shell` | Masuk MySQL CLI |
| `make log` | Lihat logs |
| `make help` | Semua commands |

## 🔐 Konfigurasi Environment

Salin `.env.example` → `.env` lalu sesuaikan:

| Variable | Wajib | Keterangan |
|----------|-------|------------|
| `DB_HOST/PORT/NAME/USER/PASS` | ✅ | Koneksi MySQL |
| `APP_USERNAME` | ✅ | Username login |
| `APP_PASSWORD` | ✅* | Password plain (*atau gunakan `APP_PASSWORD_HASH`) |
| `APP_PASSWORD_HASH` | ○ | bcrypt hash (generate: lihat bawah) |
| `SECRET_KEY` | ✅ | Signing key token — `openssl rand -hex 32` |
| `WAHA_WEBHOOK_URL` | ○ | Default endpoint WAHA |
| `DEBUG` | ○ | `false` untuk production |

Generate bcrypt hash:
```bash
python3 -c "import bcrypt; print(bcrypt.hashpw(b'password_anda', bcrypt.gensalt()).decode())"
```

## 📊 Database Schema

```
projects ─┬─< tasks ─┬─< reminders
          │          └─< notification_logs >─ webhook_configs
          └─< notification_logs
```

| Table | Fungsi |
|-------|--------|
| `projects` | name, color (hex), icon, archived, created_at |
| `tasks` | title, description, priority (enum), status (enum), deadline, completed_at |
| `reminders` | type (day_h/relative/absolute), relative_value/unit, absolute_time, sent, sent_at |
| `webhook_configs` | endpoint_url, headers (JSON), message_template, is_active |
| `notification_logs` | status (pending/sent/failed), response_code/body, retry_count |

## 🔄 Notification Flow

```
Task dibuat dengan deadline
    ↓ (auto)
Day-H reminder terbuat
    ↓ (tiap menit)
Scheduler cek semua reminder yang belum terkirim
    ↓ (jika due)
Render template → POST webhook (WAHA)
    ↓ (gagal?)
Retry exponential backoff → log hasil
    ↓
notification_logs + reminder.sent = true
```

Template variables: `{task_title}`, `{project_name}`, `{deadline}`, `{priority}`, `{status}`

## 🧪 Testing

E2E test suite lengkap (14 checks) — semua lulus:

```bash
# Pastikan MySQL + server berjalan, lalu:
bash docs/e2e_final_test.sh   # atau lihat docs/TESTING_DEPLOYMENT.md
```

Coverage: health, auth (valid/invalid/protected), project CRUD, task CRUD + auto Day-H reminder, completion toggle, stats, scheduler, notification logs, frontend, Swagger UI.

## 🚀 Deployment

Panduan production lengkap: [docs/TESTING_DEPLOYMENT.md](docs/TESTING_DEPLOYMENT.md)

```bash
# Production checklist singkat:
export SECRET_KEY="$(openssl rand -hex 32)"
export APP_PASSWORD_HASH="<bcrypt_hash>"
export WAHA_WEBHOOK_URL="https://waha-instance-anda.com/webhook"
docker compose up -d
docker compose exec dashboardku alembic upgrade head
```

### Backup & Restore Database
```bash
# Backup
docker compose exec mysql mysqldump -u root -prootpass dashboardku > backup.sql
# Restore
cat backup.sql | docker compose exec -T mysql mysql -u root -prootpass dashboardku
```

## 📈 Project Status

| Phase | Scope | Status |
|-------|-------|--------|
| 1. Foundation | Docker, MySQL, models, FastAPI | ✅ Complete |
| 2. Core CRUD | Auth, Project/Task/Reminder API | ✅ Complete |
| 3. Notification | Scheduler, webhook, retry, logging | ✅ Complete |
| 4. Frontend | SPA login + dashboard + modals | ✅ Complete |
| 5. Testing & Deployment | E2E tests, git, docs | ✅ Complete |

**Progress: 100% (5/5 phases)** — detail per phase di [PROJECT_TRACKER.md](PROJECT_TRACKER.md)

## 📚 Dokumentasi

- [CONCEPT.md](CONCEPT.md) — Spesifikasi sistem & implementation plan
- [DESIGN.md](DESIGN.md) — Design system (warna, tipografi, komponen)
- [PROJECT_TRACKER.md](PROJECT_TRACKER.md) — Tracker status semua phase
- [docs/TESTING_DEPLOYMENT.md](docs/TESTING_DEPLOYMENT.md) — Testing & production deployment
- [docs/PHASE_1-5_SUMMARY.md](docs/) — Ringkasan per phase

## 📝 License

MIT

---

**Version**: 1.0.0 | **Completed**: August 18, 2026 | **Status**: Production Ready ✅
