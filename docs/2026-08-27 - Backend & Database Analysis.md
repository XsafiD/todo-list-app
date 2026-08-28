# Analisis Backend & Skema Database — Dashboardku

> Tanggal: 2026-08-27
> Status: Analisis pasca-deployment, sebagai fondasi untuk rebuild frontend (Vanilla HTML + Tailwind CSS).
> Sumber: `app/models.py`, `app/schemas.py`, `app/main.py`, `app/security.py`, `app/api/**`, `app/services/**`, `alembic/versions/a2546b8ec0d1_initial_schema.py`

---

## 1. Ringkasan Arsitektur Backend

| Komponen | Teknologi | Lokasi |
|---|---|---|
| Web framework | FastAPI (lifespan + CORS) | `app/main.py` |
| ORM | SQLAlchemy 2.0 (Mapped/mapped_column) | `app/models.py` |
| Database | MySQL (PyMySQL, charset utf8mb4) | `app/database.py`, `app/config.py` |
| Migrasi | Alembic (1 revisi: `a2546b8ec0d1`) | `alembic/versions/` |
| Validasi | Pydantic v2 | `app/schemas.py` |
| Auth | Single-user via env, bcrypt + token HMAC-SHA256 buatan sendiri | `app/security.py`, `app/api/dependencies.py` |
| Scheduler | APScheduler (AsyncIOScheduler, cron tiap 1 menit) | `app/services/scheduler.py` |
| Notifikasi | Webhook HTTP (target utama: WAHA / WhatsApp gateway) via httpx | `app/services/webhook.py` |
| Frontend | Vanilla HTML/JS/CSS di-mount di `/static`, disajikan di `/` | `app/static/` |

Catatan penting: **tidak ada tabel `users`**. Autentikasi adalah single-user, kredensial dibaca dari environment (`APP_USERNAME`, `APP_PASSWORD`, atau `APP_PASSWORD_HASH`), sehingga skema database murni untuk domain task management + notifikasi.

---

## 2. Skema Database (5 Tabel)

### ERD

```
projects (1) ────< (N) tasks (1) ────< (N) reminders
                          │                      │
                          │ (SET NULL)           │ (SET NULL)
                          ▼                      ▼
                  notification_logs ─────► webhook_configs (SET NULL)
```

### 2.1 `projects`

| Kolom | Tipe | Constraint | Default |
|---|---|---|---|
| `id` | INT | PK, AUTO_INCREMENT | — |
| `name` | VARCHAR(255) | NOT NULL | — |
| `color` | VARCHAR(7) | NOT NULL | `'#3B82F6'` (format hex divalidasi regex di schema) |
| `icon` | VARCHAR(50) | NULL | — |
| `archived` | BOOLEAN | NOT NULL | `false` (soft-delete) |
| `created_at` | DATETIME | NOT NULL | `now()` server-side |

- Index: `idx_projects_name (name)`
- Relasi: `tasks` (lazy `selectin`)
- Perilaku delete: `DELETE /api/projects/{id}` melepas task (set `project_id = NULL`), task tidak ikut terhapus.

### 2.2 `tasks`

| Kolom | Tipe | Constraint | Default |
|---|---|---|---|
| `id` | INT | PK, AUTO_INCREMENT | — |
| `project_id` | INT | NULL, FK → `projects.id` **ON DELETE SET NULL** | — |
| `title` | VARCHAR(500) | NOT NULL | — |
| `description` | TEXT | NULL | — |
| `priority` | ENUM `task_priority` (LOW/MEDIUM/HIGH) | NOT NULL | `medium` |
| `status` | ENUM `task_status` (TODO/IN_PROGRESS/DONE) | NOT NULL | `todo` |
| `deadline` | DATETIME | NULL | — |
| `completed_at` | DATETIME | NULL | diisi otomatis saat status → DONE |
| `created_at` | DATETIME | NOT NULL | `now()` |

- Index: `idx_tasks_project_id`, `idx_tasks_deadline`, `idx_tasks_status`
- Relasi: `project` (many-to-one), `reminders` (cascade `all, delete-orphan`, lazy `selectin`)
- Task boleh tanpa project (`project_id` nullable → "inbox").

### 2.3 `reminders`

| Kolom | Tipe | Constraint | Default |
|---|---|---|---|
| `id` | INT | PK, AUTO_INCREMENT | — |
| `task_id` | INT | NOT NULL, FK → `tasks.id` **ON DELETE CASCADE** | — |
| `reminder_type` | ENUM `reminder_type` (DAY_H/RELATIVE/ABSOLUTE) | NOT NULL | — |
| `relative_value` | INT | NULL (> 0 divalidasi di schema) | — |
| `relative_unit` | ENUM `reminder_unit` (MINUTES/HOURS/DAYS) | NULL | — |
| `absolute_time` | DATETIME | NULL | — |
| `sent` | BOOLEAN | NOT NULL | `false` |
| `sent_at` | DATETIME | NULL | — |

- Index: `idx_reminders_task_id`
- Kolom `relative_*` dan `absolute_time` saling eksklusif berdasarkan `reminder_type` (divalidasi di layer Pydantic & route, bukan DB constraint).
- Aturan bisnis:
  - **day_h**: otomatis dibuat/dihapus oleh API task jika task punya/tidak punya deadline (`_sync_day_h_reminder`); duplikat day_h ditolak 409.
  - Reminder yang sudah `sent` tidak boleh diubah/dihapus (409).

### 2.4 `webhook_configs`

| Kolom | Tipe | Constraint | Default |
|---|---|---|---|
| `id` | INT | PK, AUTO_INCREMENT | — |
| `name` | VARCHAR(255) | NULL | — |
| `endpoint_url` | VARCHAR(2048) | NOT NULL | — |
| `headers` | TEXT (JSON string) | NULL | — |
| `message_template` | TEXT | NULL | placeholder `{task_title}`, `{project_name}`, `{deadline}`, dll. |
| `is_active` | BOOLEAN | NOT NULL | `true` |
| `created_at` | DATETIME | NOT NULL | `now()` |
| `updated_at` | DATETIME | NULL, `onupdate=now()` | — |

- Index: `idx_webhook_config_active`
- Semantik: **satu config aktif per sistem** — `POST /api/webhook/config` berperilaku upsert terhadap config aktif.

### 2.5 `notification_logs`

| Kolom | Tipe | Constraint | Default |
|---|---|---|---|
| `id` | INT | PK, AUTO_INCREMENT | — |
| `task_id` | INT | NULL, FK → `tasks.id` SET NULL | — |
| `reminder_id` | INT | NULL, FK → `reminders.id` SET NULL | — |
| `webhook_config_id` | INT | NULL, FK → `webhook_configs.id` SET NULL | — |
| `status` | ENUM `notification_status` (PENDING/SENT/FAILED) | NOT NULL | `pending` |
| `response_code` | INT | NULL | — |
| `response_body` | TEXT | NULL | — |
| `retry_count` | INT | NOT NULL | `0` (belum pernah dipakai) |
| `created_at` | DATETIME | NOT NULL | `now()` |

- Index: `task_id`, `reminder_id`, `webhook_config_id`, `status`, `created_at`
- Berfungsi sebagai audit trail pengiriman notifikasi (tetap ada walau task/reminder/webhook dihapus — FK SET NULL).

---

## 3. Enum & Perilaku Penyimpanannya (Catatan Penting)

Enum Python didefinisasi sebagai `str, Enum` dengan **value lowercase** (`low`, `todo`, `day_h`), tetapi SQLAlchemy secara default menyimpan **nama member** (`LOW`, `TODO`, `DAY_H`) — terlihat di migrasi Alembic (`sa.Enum('LOW','MEDIUM','HIGH', ...)`). Konsekuensi:

- API menerima/mengembalikan string lowercase (Pydantic menangani konversi).
- Query filter `TaskStatus(status_filter)` di route memakai value, SQLAlchemy yang menerjemahkan ke nama DB — konsisten selama membaca lewat ORM.
- Hindari query SQL mentah yang berasumsi nilai lowercase di kolom enum.

---

## 4. Autentikasi

- **Single user** dari env: `APP_USERNAME` / `APP_PASSWORD` (atau `APP_PASSWORD_HASH` pre-hashed bcrypt, di-cache `lru_cache`).
- `POST /api/login` → `{access_token, token_type: "bearer", expires_in, username}`.
- Token: format JWT-like buatan sendiri — `base64url(payload).base64url(hmac_sha256)` dengan payload `username:expires_at`, TTL **30 hari**. Bukan JWT standar (tanpa header, tanba `sub`/`iss`).
- `require_auth` menerima 3 skema (di `app/api/dependencies.py`):
  1. `Authorization: Bearer <token>`
  2. `Authorization: Basic base64(user:pass)`
  3. `X-API-Key: <token>`
- Semua route domain (projects/tasks/reminders/webhooks/stats) dilindungi; `/health`, `/scheduler/status`, `/`, `/static` terbuka.

---

## 5. Inventaris API Endpoint

| Method | Path | Auth | Keterangan |
|---|---|---|---|
| POST | `/api/login` | — | Tukar kredensial → bearer token |
| GET | `/api/me` | ✅ | Info user aktif |
| GET | `/api/projects?include_archived=` | ✅ | List project (default exclude archived) |
| POST | `/api/projects` | ✅ | Buat project (201) |
| GET/PUT | `/api/projects/{id}` | ✅ | Detail / update partial |
| PATCH | `/api/projects/{id}/archive?archived=` | ✅ | Soft (un)archive |
| DELETE | `/api/projects/{id}` | ✅ | Hapus project, task dilepas (project_id=NULL) |
| GET | `/api/tasks?status_filter=&project_id=` | ✅ | Semua task + filter |
| GET/POST | `/api/projects/{id}/tasks` | ✅ | Task per project (404 jika project tak ada) |
| GET/PUT/DELETE | `/api/tasks/{id}` | ✅ | CRUD task; PUT menjaga `completed_at` konsisten |
| PATCH | `/api/tasks/{id}/complete` | ✅ | Toggle done ↔ todo |
| GET/POST | `/api/tasks/{id}/reminders` | ✅ | List/buat reminder (day_h duplikat → 409) |
| PUT/DELETE | `/api/reminders/{id}` | ✅ | Ubah/hapus (409 jika sudah sent) |
| GET/POST | `/api/webhook/config` | ✅ | List / upsert config aktif |
| GET | `/api/webhook/test` | ✅ | Kirim notifikasi tes ke endpoint aktif |
| GET | `/api/notifications/logs` | ✅ | Log dengan `limit/offset/status_filter/task_id` |
| GET | `/api/stats` | ✅ | total/active/completed/overdue tasks + total/active projects |
| GET | `/health`, `/scheduler/status` | — | Sistem |

---

## 6. Alur Notifikasi (Scheduler)

1. APScheduler menjalankan `check_and_notify_deadlines()` tiap menit (cron `minute="*"`).
2. Ambil semua task dengan `status != DONE` + reminders eager-load (`selectin`).
3. Untuk tiap reminder yang belum `sent`, cek jadwal trigger:
   - **day_h** → trigger saat tanggal deadline == tanggal hari ini (perbandingan kalender, pakai `datetime.now()` lokal).
   - **relative** → `now >= deadline - (value unit)`.
   - **absolute** → `now >= absolute_time`.
4. `process_reminder()`: tandai `sent=True, sent_at`, render pesan dari `message_template` config aktif, kirim via `send_webhook()`, catat hasil ke `notification_logs` (SENT/FAILED).

---

## 7. Temuan & Risiko (dipertahankan untuk evaluasi saat rebuild)

### Bug / inkonsistensi nyata

1. **Scheduler tidak memakai config webhook** — `process_reminder` mem-parse `headers` dari config tapi memanggil `send_webhook(message, context)` **tanpa** `endpoint_url`/`headers`; `webhook_sender.base_url` kosong sehingga reminder nyata hampir pasti gagal dengan `"No webhook URL configured"` dan tercatat FAILED. (Route `/api/webhook/test` benar karena meneruskan `endpoint_url`.)
2. **`get_db` ganda** — `app/api/dependencies.py` punya `get_db` sendiri dengan `lru_cache` pada satu session (berbahaya: session dibagikan antar request). Untungnya semua route memakai `app.database.get_db`; versi dependencies adalah dead code yang sebaiknya dihapus.
3. **Template placeholder hardcoded** — `{priority}`, `{status}`, `{reminder_type}` di `notification.py` diisi nilai statis ("medium"/"todo"/"day_h"), bukan nilai sebenarnya dari task/reminder.
4. **`retry_count` & `retry_notification` tidak terpakai** — mekanisme retry dengan exponential backoff ada di `webhook.py` tapi scheduler tidak memanggilnya; kolom `retry_count` selalu 0.
5. **Race/kondisi gagal-kirim** — `sent=True` di-set **sebelum** pengiriman; jika proses crash setelah set tapi sebelum commit log, reminder bisa terlewat tanpa jejak. `db_session.commit()` hanya di akhir loop; jika ada exception di tengah, semua status bisa batch-rollback/berubah bersama.

### Keputusan desain yang perlu disadari

6. **CORS terlalu terbuka** — `allow_origins=["*"]` sekaligus `allow_credentials=True` (kombinasi tidak valid menurut spec CORS; browser akan tolak kredensial).
7. **Timezone campur** — scheduler memakai `datetime.now()` (lokal) untuk day_h vs `datetime.utcnow()` untuk pembanding lain; di server non-UTC perilaku day_h bergeser.
8. **Enum names vs values** (lihat §3) — perlu konsistensi bila nanti query raw SQL / report.
9. **Tanpa `updated_at` di tasks** — sorting selalu `created_at desc`; tidak ada histori perubahan.
10. **`PATCH /complete` toggle dua arah** — DONE → TODO (bukan IN_PROGRESS); frontend harus aware.
11. **Token 30 hari tanpa refresh/logout server-side** — cukup untuk personal app, tapi tidak ada mekanisme revoke.
12. **`POST /api/webhook/config` upsert implisit** — body tanpa field tidak mengubah apa pun; frontend sebaiknya selalu kirim field lengkap.

---

## 8. Implikasi untuk Rebuild Frontend

- Data model inti untuk UI: **Project → Task → Reminder**, plus panel **Webhook Config** & **Notification Logs**, dan **Stats** untuk dashboard cards.
- Task tanpa project (`project_id: null`) harus punya tempat di UI (konsep "Inbox/Unassigned").
- Status task: `todo | in_progress | done`; priority: `low | medium | high` — cocok untuk badge/filter Tailwind.
- Response API konsisten camel/snake mix (semua snake_case) dan langsung dari Pydantic `from_attributes` — mudah dipetakan ke render Vanilla JS.
- Auth flow frontend: simpan `access_token` (localStorage/sessionStorage), kirim `Authorization: Bearer <token>`; tangani 401 → redirect ke login.
- Endpoint yang wajib dikonsumsi UI baru: `login`, `me`, `projects` CRUD + archive, `tasks` CRUD + complete + filter, `reminders` per task, `webhook/config` + test, `notifications/logs`, `stats`.

---

## 9. Kesimpulan

Skema database sudah solid untuk kebutuhan personal task dashboard (5 tabel, FK behavior jelas: SET NULL untuk historis, CASCADE untuk reminder milik task). Masalah utama berada di **integrasi scheduler → webhook** (endpoint tidak diteruskan) dan beberapa dead code / praktik berisiko (double `get_db`, CORS, timezone). Backend tidak perlu dirombak total untuk rebuild frontend, tapi item di §7 sebaiknya diperbaiki bertahap karena notifikasi adalah fitur inti aplikasi ini.
