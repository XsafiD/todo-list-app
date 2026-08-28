# Dashboardku 🚀

Personal Task Management System dengan project organization, task tracking, dan dashboard analytics — pengganti Todoist yang bisa dikustomisasi penuh.

![Status](https://img.shields.io/badge/status-beta-yellow) ![Phases](https://img.shields.io/badge/phases-3%2F5%20complete-blue) ![License](https://img.shields.io/badge/license-MIT-lightgrey) ![Flask](https://img.shields.io/badge/flask-3.0.3-green)

## ✨ Fitur

- **Task Management** — CRUD task dengan priority, status, deadline, dan auto-completion timestamp
- **Project Organization** — project berwarna dengan soft-delete (archive)
- **Dashboard Analytics** — stats cards (total, completed, overdue), project grid, task overview
- **Smart Filtering** — filter task by project, status, priority dengan autosubmit
- **Task State Machine** — todo → in_progress → done dengan toggle complete
- **Day-H Reminder** — reminder otomatis di hari deadline (auto-created)
- **Single-User Auth** — bcrypt password + Flask cookie-based session
- **Responsive Design** — mobile-first dengan bottom nav, FAB, modal full-screen
- **Accessibility** — Lighthouse a11y 100, keyboard shortcuts (n=task baru, /=filter), ARIA labels

## 🛠️ Tech Stack

| Layer | Teknologi |
|-------|-----------|
| Backend | Flask 3.0.3, Flask-SQLAlchemy, Flask-WTF, Jinja2 |
| Database | MySQL 8.0 (Docker) |
| Frontend | Vanilla HTML + Tailwind CSS (CDN) + Font Awesome v6 (CDN) |
| JavaScript | Vanilla JS (IIFE, strict-mode, no framework) |
| Testing | pytest, conftest SQLite in-memory |
| Deployment | Docker (MySQL only for now) |

## ⚡ Quick Start

### Local Development (via venv)

```bash
# 1. Setup environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Konfigurasi
cp .env.example .env

# 3. Start MySQL via Docker
docker compose up -d mysql

# 4. Migrasi database
alembic upgrade head

# 5. Seed default user
flask create-user

# 6. Jalankan Flask dev server
flask run
```

**Akses aplikasi**: http://localhost:5000

**Default login**: `admin` / `changeme` — **ganti di `.env` sebelum production!**

### Makefile Shortcut

```bash
# Semua langkah di atas dalam satu command
make mysql-up && make migrate-up && make seed-user && make dev
```

## 📁 Project Structure

```
dashboardku/
├── app/
│   ├── __init__.py              # Flask app factory + blueprint register
│   ├── config.py                # Flask config (env-based)
│   ├── extensions.py            # db, csrf instances
│   ├── models.py                # ORM models (User, Project, Task, Reminder, NotificationLog)
│   ├── controllers/             # Blueprint per domain
│   │   ├── auth_controller.py   # auth_bp: login, logout
│   │   ├── project_controller.py# project_bp: CRUD + archive + dashboard
│   │   └── task_controller.py   # task_bp: CRUD + complete toggle
│   ├── services/                # Business Layer
│   │   ├── auth_service.py      # verify_credentials, session management
│   │   ├── project_service.py   # CRUD + archive
│   │   └── task_service.py      # CRUD + toggle + day_h sync
│   ├── forms/                   # WTForms
│   │   ├── auth_forms.py
│   │   ├── project_forms.py
│   │   └── task_forms.py
│   ├── templates/               # Jinja2 templates
│   │   ├── base.html
│   │   ├── components/          # badge, card, form, modal, navbar
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── project/
│   │   └── task/
│   ├── static/
│   │   ├── css/style.css        # Tailwind CDN + custom
│   │   └── js/
│   │       ├── app.js
│   │       ├── modal.js
│   │       ├── form.js
│   │       ├── dashboard.js
│   │       ├── task.js
│   │       └── shortcuts.js
│   └── utils/
│       ├── decorators.py        # login_required
│       └── filters.py           # Custom Jinja2 filters
├── alembic/                     # Migrations
├── archive/                     # Kode FastAPI lama (referensi history)
├── docs/                        # Phase summaries, coding standards
├── DESIGN.md                    # Design system (warna, tipografi, komponen)
├── docker-compose.yml           # MySQL service only
├── Makefile
└── requirements.txt
```

## 🌐 Routes

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET/POST | `/auth/login` | Login form / submit |
| GET | `/auth/logout` | Logout |
| GET | `/` | Dashboard (stats + project grid) |
| GET | `/projects` | List semua project |
| GET/POST | `/projects/create` | Form buat project |
| GET/POST | `/projects/<id>/edit` | Form edit project |
| POST | `/projects/<id>/delete` | Hapus project |
| POST | `/projects/<id>/archive` | Archive/unarchive |
| GET | `/projects/<id>` | Detail project + task list |
| GET | `/tasks` | List semua task (+filter project/status/priority) |
| GET/POST | `/tasks/create` | Form buat task |
| GET/POST | `/tasks/<id>/edit` | Form edit task |
| POST | `/tasks/<id>/delete` | Hapus task |
| POST | `/tasks/<id>/complete` | Toggle completion (AJAX/PRG fallback) |
| GET | `/tasks/<id>` | Detail task |
| GET | `/health` | Health check |

## 🔧 Makefile Commands

| Command | Deskripsi |
|---------|-----------|
| `make dev` | Jalankan Flask dev server (venv, port 5000) |
| `make mysql-up` / `mysql-down` | Start/stop MySQL container |
| `make migrate-up` / `migrate-down` | Apply/rollback migrations |
| `make migrate-revision MESSAGE="..."` | Buat migration baru |
| `make seed-user` | Create/reset seed user (dari .env) |
| `make mysql-shell` | Masuk MySQL CLI |
| `make mysql-logs` | Lihat MySQL logs |
| `make help` | Semua commands |

## 🔐 Konfigurasi Environment

Salin `.env.example` → `.env` lalu sesuaikan:

| Variable | Wajib | Keterangan |
|----------|-------|------------|
| `DB_HOST/PORT/NAME/USER/PASS` | ✅ | Koneksi MySQL |
| `APP_USERNAME` | ✅ | Username login |
| `APP_PASSWORD` | ✅* | Password plain (*atau gunakan `APP_PASSWORD_HASH`) |
| `APP_PASSWORD_HASH` | ○ | bcrypt hash (generate: lihat bawah) |
| `SECRET_KEY` | ✅ | Flask secret key — `openssl rand -hex 32` |
| `DEBUG` | ○ | `false` untuk production |

Generate bcrypt hash:
```bash
python3 -c "import bcrypt; print(bcrypt.hashpw(b'password_anda', bcrypt.gensalt()).decode())"
```

## 📊 Database Schema

```
users ─< projects ─< tasks ─< reminders
        └─< notification_logs
```

| Table | Fungsi |
|-------|--------|
| `users` | username, password_hash (bcrypt), created_at |
| `projects` | name, color (hex), icon, archived, created_at |
| `tasks` | title, description, priority (enum), status (enum), deadline, completed_at |
| `reminders` | type (day_h/relative/absolute), relative_value/unit, absolute_time, sent, sent_at |
| `notification_logs` | status (pending/sent/failed), response_code/body, retry_count |

## 🔄 Task Flow

```
Task dibuat dengan deadline
    ↓ (auto)
Day-H reminder terbuat (di database)
    ↓ (user action)
Task di-mark complete / reopened
    ↓ (state machine)
Status berubah + completed_at di-set/unset
```

**Note**: Notification & scheduler akan diimplementasikan di Phase 4 (pending).

## 🧪 Testing

Test suite lengkap dengan pytest — semua lulus:

```bash
# Jalankan test (pastikan .venv aktif)
.venv/bin/python -m pytest -v
```

Coverage (43/43 pass):
- **Auth** (8 test): login valid/invalid, session, protected routes, seed user
- **Projects** (11 test): CRUD, archive, count, filter
- **Tasks** (14 test): CRUD, toggle complete, state machine, Day-H sync, deadline overdue
- **Stats** (3 test): dashboard count queries, aggregate performance
- **Integration** (7 test): PRG pattern, flash messages, AJAX JSON responses, anti N+1

## 🚀 Deployment

**Phase 5 (Pending)** — Deployment Docker akan diimplementasikan setelah Phase 4 selesai.

**Untuk sekarang**: Gunakan development mode via venv (lihat Quick Start di atas).

**Future checklist**:
- Dockerfile dengan gunicorn
- docker-compose.yml (service aplikasi + MySQL)
- HTTPS (reverse proxy Caddy/nginx)
- Rate limiting login
- Hardening security headers

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
| 1. Foundation | Flask, MySQL, models, auth | ✅ Complete |
| 2. Connect Real DB | ORM, aggregate queries, Day-H sync | ✅ Complete |
| 3. Frontend Polish | Skeleton, AJAX toggle, shortcuts, a11y | ✅ Complete |
| 4. Notification & Scheduler | Webhook, retry, logging, settings | ⏳ Pending |
| 5. Deployment Docker | Dockerfile, docker-compose, production | ⏳ Pending |

**Progress: 60% (3/5 phases)** — detail per phase di [docs/2026-08-27 - Rencana Migrasi Flask.md](docs/2026-08-27%20-%20Rencana%20Migrasi%20Flask.md)

## 📚 Dokumentasi

- [DESIGN.md](DESIGN.md) — Design system (warna, tipografi, komponen, shortcuts)
- [AGENTS.md](AGENTS.md) — Coding standards + mapping archetype
- [docs/2026-08-27 - Rencana Migrasi Flask.md](docs/2026-08-27%20-%20Rencana%20Migrasi%20Flask.md) — Roadmap lengkap 5 phase
- [docs/coding-standards/](docs/coding-standards/) — Rule files untuk controller, service, model, view, form, dll.

## 📝 License

MIT

---

**Version**: 2.0.0 (Flask) | **Updated**: August 27, 2026 | **Status**: Beta ✅
