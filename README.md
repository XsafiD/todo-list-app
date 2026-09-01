# Dashboardku 🚀

Personal Task Management System dengan project organization, task tracking, dan dashboard analytics — pengganti Todoist yang bisa dikustomisasi penuh.

![Status](https://img.shields.io/badge/status-beta-yellow) ![Phases](https://img.shields.io/badge/phases-4%2F5%20complete-blue) ![License](https://img.shields.io/badge/license-MIT-lightgrey) ![Flask](https://img.shields.io/badge/flask-3.0.3-green)

## ✨ Fitur

- **Task Management** — CRUD task dengan priority, status, deadline, dan auto-completion timestamp
- **Project Organization** — project berwarna dengan soft-delete (archive)
- **Dashboard Analytics** — stats cards (total, completed, overdue), project grid, task overview
- **Tugas Kanban** — board 3 kolom (Todo/Proses/Selesai) drag & drop SortableJS, warna kolom per status, fallback tombol pindah
- **Arsip** — arsipkan tugas selesai dari Kanban + arsip otomatis harian 23:59 (APScheduler, toggle di Pengaturan)
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
| Deployment | Docker Compose — dev: MySQL only; prod: gunicorn + MySQL |

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

# 5. Jalankan Flask dev server
flask run
```

**Akses aplikasi**: http://localhost:5000

**Setup awal**: Buka browser → akan otomatis redirect ke halaman "Buat Akun" untuk membuat akun pertama (hanya sekali). Setelah itu, login seperti biasa.

### Makefile Shortcut

```bash
# Semua langkah di atas dalam satu command
make mysql-up && make migrate-up && make dev
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
│   │   ├── css/style.css        # Custom styles (state card, toast, kanban)
│   │   └── js/
│   │       ├── app.js
│   │       ├── modal.js
│   │       ├── form.js
│   │       ├── dashboard.js
│   │       ├── task.js
│   │       ├── kanban.js        # Drag & drop board (SortableJS)
│   │       ├── toast.js
│   │       └── shortcuts.js
│   └── utils/
│       ├── decorators.py        # login_required
│       └── filters.py           # Custom Jinja2 filters
├── alembic/                     # Migrations
├── archive/                     # Kode FastAPI lama (referensi history)
├── docs/                        # Phase summaries, coding standards, rencana
├── DESIGN.md                    # Design system (warna, tipografi, komponen)
├── Dockerfile                   # Image production (gunicorn, non-root)
├── docker-compose.yml           # Dev: MySQL only
├── docker-compose.prod.yml      # Prod: app + MySQL
├── entrypoint.sh                # wait-for-DB → alembic → gunicorn
├── scripts/backup_db.sh         # Backup harian mysqldump (cron)
├── Makefile
└── requirements.txt
```

## 🌐 Routes

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET/POST | `/auth/setup` | Setup awal — buat akun pertama (hanya saat users kosong, setelah itu 404) |
| GET/POST | `/auth/login` | Login form / submit |
| POST | `/auth/logout` | Logout |
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
| GET | `/tasks/kanban` | Board kanban 3 kolom drag & drop |
| POST | `/tasks/<id>/status` | Ubah status (AJAX dari kanban) |
| POST | `/tasks/<id>/archive` | Arsipkan tugas selesai |
| GET | `/arsip` | Riwayat arsip (+ unarchive/hapus permanen) |
| GET | `/pengaturan` | Toggle arsip otomatis + status scheduler |
| GET | `/tasks/<id>` | Detail task |
| GET | `/health` | Health check |

## 🔧 Makefile Commands

| Command | Deskripsi |
|---------|-----------|
| `make dev` | Jalankan Flask dev server (venv, port 5000) |
| `make mysql-up` / `mysql-down` | Start/stop MySQL container |
| `make migrate-up` / `migrate-down` | Apply/rollback migrations |
| `make migrate-revision MESSAGE="..."` | Buat migration baru |
| `make mysql-shell` | Masuk MySQL CLI |
| `make mysql-logs` | Lihat MySQL logs |
| `make help` | Semua commands |

## 🔐 Konfigurasi Environment

Salin `.env.example` → `.env` lalu sesuaikan:

| Variable | Wajib | Keterangan |
|----------|-------|------------|
| `DB_HOST/PORT/NAME/USER/PASS` | ✅ | Koneksi MySQL |
| `SECRET_KEY` | ✅ | Flask secret key — `openssl rand -hex 32` |
| `DEBUG` | ○ | `false` untuk production |
| `SESSION_COOKIE_SECURE` | ○ | `true` di production (HTTPS via cloudflared/tailscale) |
| `SCHEDULER_ENABLED` | ○ | Default `true`; `false` untuk mematikan auto-archive |

> Tidak ada seed user dari env — akun pertama dibuat lewat halaman setup awal
> di browser (`/auth/setup`, aktif hanya saat tabel `users` kosong).

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

**Note**: Arsip otomatis via scheduler sudah jalan (toggle di Pengaturan); pengiriman notifikasi webhook akan diimplementasikan di Phase 4.

## 🧪 Testing

Test suite lengkap dengan pytest — semua lulus:

```bash
# Jalankan test (pastikan .venv aktif)
.venv/bin/python -m pytest -v
```

Coverage (104 test pass): auth & session, projects CRUD/archive, tasks CRUD + state machine + Day-H sync,
kanban board & endpoint status, arsip & auto-archive scheduler, settings, dashboard stats,
integrasi PRG/flash/AJAX JSON, anti N+1.

## 🚀 Deployment (Docker Production)

Stack production: **app (gunicorn, non-root) + MySQL 8.0** via `docker-compose.prod.yml`.
Detail lengkap arsitektur & runbook: [docs/2026-08-29 - Rencana Deployment Production.md](docs/2026-08-29%20-%20Rencana%20Deployment%20Production.md)

```bash
# 1. Siapkan env production (di server, gitignored)
cp .env.production.example .env.production && $EDITOR .env.production && chmod 600 .env.production

# 2. Naikkan stack (entrypoint: wait-for-DB → alembic upgrade → gunicorn)
docker compose -f docker-compose.prod.yml up -d --build

# 3. Setup awal — buka http://<server>:5000 di browser, buat akun pertama
#    (halaman "Buat Akun" muncul otomatis; hanya sekali, setelah itu 404)

# 4. Verifikasi
curl -s http://localhost:5000/health
docker compose -f docker-compose.prod.yml ps   # keduanya healthy
```

Catatan desain:
- **Scheduler aman** — gunicorn 1 worker + 4 threads (job arsip otomatis tepat jalan 1x) + `TZ=Asia/Jakarta`
- **MySQL tanpa published port** — akses admin via `docker compose exec`
- **Migrasi otomatis** saat container start (idempoten), volume `mysql_prod_data` terpisah dari dev
- **ProxyFix** aktif — cocok di belakang cloudflared / tailscale serve (1 hop)

### Backup & Restore Database

```bash
# Backup harian (gzip → ./backups/, keep 7 hari) — untuk cron
./scripts/backup_db.sh

# Restore
gunzip -c backups/db-YYYY-MM-DD.sql.gz | \
  docker compose -f docker-compose.prod.yml exec -T mysql mysql -u root -p"$MYSQL_ROOT_PASSWORD" "$DB_NAME"
```

Dev (MySQL via docker-compose.yml):
```bash
docker compose exec mysql mysqldump -u root -prootpass dashboardku > backup.sql
cat backup.sql | docker compose exec -T mysql mysql -u root -prootpass dashboardku
```

## 📈 Project Status

| Phase | Scope | Status |
|-------|-------|--------|
| 1. Foundation | Flask, MySQL, models, auth | ✅ Complete |
| 2. Connect Real DB | ORM, aggregate queries, Day-H sync | ✅ Complete |
| 3. Frontend Polish | Skeleton, AJAX toggle, shortcuts, a11y | ✅ Complete |
| 4. Notification & Scheduler | Webhook, retry, logging | ⏳ Parsial (arsip otomatis + Pengaturan jalan; notifikasi menyusul) |
| 5. Deployment Docker | Dockerfile, docker-compose, production | ✅ Complete (2026-08-30) |

**Progress: 80% (4/5 phases)** — detail per phase di [docs/archive/2026-08-27 - Rencana Migrasi Flask.md](docs/archive/2026-08-27%20-%20Rencana%20Migrasi%20Flask.md) (roadmap selesai tereksekusi, diarsipkan)

## 📚 Dokumentasi

- [DESIGN.md](DESIGN.md) — Design system (warna, tipografi, komponen, shortcuts)
- [AGENTS.md](AGENTS.md) — Coding standards + mapping archetype
- [docs/archive/2026-08-27 - Rencana Migrasi Flask.md](docs/archive/2026-08-27%20-%20Rencana%20Migrasi%20Flask.md) — Roadmap 5 phase migrasi (selesai, diarsipkan)
- [docs/2026-08-29 - Rencana Deployment Production.md](docs/2026-08-29%20-%20Rencana%20Deployment%20Production.md) — Arsitektur deploy, runbook, backup
- [docs/coding-standards/](docs/coding-standards/) — Rule files untuk controller, service, model, view, form, dll.

## 📝 License

MIT

---

**Version**: 2.1.0 (Flask + Docker prod) | **Updated**: August 30, 2026 | **Status**: Beta ✅
