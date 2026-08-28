# Rencana Migrasi FastAPI → Flask — Dashboardku

> Tanggal: 2026-08-27
> Status: APPROVED — semua pertanyaan §5 sudah dijawab, eksekusi berjalan
> Prasyarat baca: `docs/2026-08-27 - Backend & Database Analysis.md`, `AGENTS.md`, `docs/coding-standards/coding-rules/_INDEX.md`
> Scope: Phase 1 view-first dengan mock data; notifikasi & scheduler di-disable; skema database inti tetap + PENAMBAHAN tabel `users` (satu-satunya perubahan); styling mengikuti `DESIGN.md`

---

## 0. Keputusan Terverifikasi (dari diskusi)

| # | Keputusan | Status |
|---|-----------|--------|
| 1 | Flask SAJA sekarang; FastAPI skip (rencana mobile API menyusul, tidak direncanakan) | ✅ |
| 2 | Flask default (Jinja2 + WTForms + session), rombak habis, ikuti coding standards `docs/coding-standards/` | ✅ |
| 3 | Arsitektur terpisah — hanya Flask yang aktif | ✅ |
| 4 | Auth: cookie-based session ala Flask (bukan token) | ✅ |
| 5 | Notifikasi & scheduler: disable, kode lama dipertahankan sebagai referensi history | ✅ |
| 6 | Fokus view dulu — mock data placeholder, data real menyusul | ✅ |
| 7 | Skema database inti tetap, MySQL tetap via Docker | ✅ |
| 8 | **[Jawaban P1]** Port aplikasi: 5000 | ✅ |
| 9 | **[Jawaban P2]** Auth pakai model DB — **tambah tabel `users`** (via migrasi Alembic baru; fitur tambah user dilupakan dulu, hanya tabel + user seed) | ✅ |
| 10 | **[Jawaban P3]** Session: cookie signed (Flask default) | ✅ |
| 11 | **[Jawaban P4]** Mock data: placeholder (beberapa project + task contoh) | ✅ |
| 12 | **[Jawaban P5]** Tailwind via CDN; **SEMUA ikon pakai Font Awesome v6 via CDNJS — emoji sebagai ikon DILARANG** | ✅ |
| 13 | **[Jawaban P6]** Kode lama pindah ke `archive/` agar struktur kerja rapi & bersih | ✅ |
| 14 | **[Jawaban P7]** Development pakai `.venv` lokal; Docker hanya untuk MySQL; Dockerfile/app container di akhir saat aplikasi jadi | ✅ |
| 15 | Styling frontend tetap mengikuti `DESIGN.md` (tokens warna, tipografi Inter, spacing, komponen) | ✅ |

---

## 1. Mapping Archetype → Domain Dashboardku

Mengikuti `_GLOSSARY.md` — diisi saat project dimulai (update juga tabel di `AGENTS.md` saat eksekusi):

| Archetype | Domain Dashboardku | Catatan |
|-----------|-------------------|---------|
| Actor | User (model DB, tabel `users` BARU) | Seed via CLI `flask create-user`; fitur tambah user menyusul |
| AdminRole | — (tidak ada, single-user) | Tidak perlu role check / `admin_required` |
| Entity | Project | Master data referensi |
| Transaction | Task | Punya state machine status |
| TransactionLine | Reminder | Detail 1-N milik Task |
| Notification | NotificationLog | DISABLE di Phase 1 |
| State Machine | TaskStatus: `todo → in_progress → done` | Delegasi ke method model |
| Boundary | Blueprint (`auth_bp`, `project_bp`, `task_bp`) | Suffix `_bp` + `url_prefix` |
| Business Layer | Service (`AuthService`, `ProjectService`, `TaskService`) | Stateless, controller tipis |
| Soft Delete | `archived` di Project | Task tidak soft-delete, pakai status |

Rule files yang jadi acuan utama: `01-controller.md`, `03-service.md`, `04-view.md`, `05-form.md`, `06-decorator.md`, `12-ajax-js.md`, `16-security.md` (+ `07-config.md`, `08-exception.md`, `14-middleware-filters.md` saat implementasi).

---

## 2. Struktur Folder Baru (Flask)

```
app/
├── __init__.py                 # Flask app factory + blueprint register loop
├── config.py                   # Flask config (env-based, ganti Pydantic Settings)
├── extensions.py               # Init db, csrf (Flask-SQLAlchemy, Flask-WTF)
├── models.py                   # ORM models (adaptasi Flask-SQLAlchemy, SKEMA TETAP)
│
├── controllers/                # Boundary — Blueprint per domain
│   ├── auth_controller.py      # auth_bp: login, logout
│   ├── project_controller.py   # project_bp: CRUD + archive + dashboard (/)
│   └── task_controller.py      # task_bp: CRUD + complete toggle
│
├── services/                   # Business Layer
│   ├── auth_service.py         # verify_credentials, session management
│   ├── project_service.py      # CRUD + archive (mock dulu)
│   └── task_service.py         # CRUD + toggle + day_h sync (mock dulu)
│
├── forms/                      # WTForms
│   ├── auth_forms.py           # LoginForm
│   ├── project_forms.py        # CreateProjectForm, EditProjectForm
│   └── task_forms.py           # CreateTaskForm, EditTaskForm
│
├── templates/                  # Jinja2 — lihat §2.1
├── static/
│   ├── css/style.css           # Tailwind CDN + custom (dari DESIGN.md)
│   └── js/
│       ├── app.js              # IIFE utama + DOM ready gate
│       ├── modal.js            # Modal pattern (open/close/Escape/scroll-lock)
│       ├── form.js             # Validasi + AJAX submit (mock dulu)
│       └── dashboard.js        # Stats cards, project grid behavior
│
└── utils/
    ├── decorators.py           # login_required
    └── filters.py              # Custom Jinja2 filters (format tanggal, warna prioritas)

archive/                        # Kode FastAPI lama — referensi history, TIDAK dihapus
├── fastapi_main.py             # (app/main.py lama)
├── fastapi_api/                # (app/api/ lama: routes + dependencies)
├── scheduler_disabled.py       # (app/services/scheduler.py lama)
├── webhook_disabled.py         # (app/services/webhook.py lama)
└── notification_disabled.py    # (app/services/notification.py lama)
```

### 2.1 Struktur Templates (sesuai `04-view.md`)

```
templates/
├── base.html                   # Layout induk: navbar + flash + block content
├── error.html                  # Halaman error global (403/404/500)
├── components/                 # Macro reusable lintas domain
│   ├── badge.html              # status_badge, priority_badge, deadline_badge
│   ├── card.html               # project_card, task_item
│   ├── form.html               # field macro (text, textarea, select, date)
│   ├── modal.html              # confirm_delete modal
│   └── navbar.html
├── auth/
│   └── login.html
├── dashboard/
│   └── index.html              # Stats cards + project grid (mock)
├── project/
│   ├── list.html
│   ├── detail.html             # Stats project + task list
│   ├── create.html
│   └── edit.html
└── task/
    ├── list.html               # Filters (project/status/priority) + task stack
    ├── detail.html             # Detail + placeholder reminders
    ├── create.html
    └── edit.html
```

Inheritance maksimal 3 level: `base.html` → domain layout → page. URL selalu `url_for()`.

---

## 3. Perubahan File

### 📦 Baru
- `app/__init__.py` — app factory + register blueprint terpusat (loop + try/except ImportError)
- `app/config.py` — class-based Flask config per environment
- `app/extensions.py` — instance `db`, `csrf`
- `app/controllers/*` — 3 blueprint
- `app/services/*` — 3 service class (stateless, error kontrak `ValueError`)
- `app/forms/*` — WTForms + CSRF
- `app/templates/**` — lihat §2.1
- `app/static/js/*` — 4 modul JS (IIFE + `"use strict"`, behavior via `data-*`)

### 🔄 Diubah
- `app/models.py` — adaptasi ke Flask-SQLAlchemy (`db.Model`), **kolom & relasi TIDAK berubah**
- `requirements.txt` — keluarkan FastAPI/uvicorn/pydantic-settings/APScheduler/httpx; masukkan Flask, Flask-SQLAlchemy, Flask-WTF, python-dotenv, gunicorn (bcrypt tetap)
- `Dockerfile` — CMD gunicorn
- `docker-compose.yml` — app port 5000 (konfirmasi §5 P1), MySQL service tetap
- `.env.example` — sesuaikan env Flask
- `Makefile` — target `dev`/`run` ke Flask
- `AGENTS.md` — isi tabel mapping archetype (§1)

### 🗄️ Dipindah ke `archive/` (disable, tidak dihapus)
- `app/main.py`, `app/api/**` (routes + dependencies + schemas-nya), `app/services/{scheduler,webhook,notification}.py`, `app/schemas.py`, `app/security.py` (token HMAC — diganti session), `app/static/{index.html,js/app.js,css/style.css}` (frontend SPA lama)
- `alembic/` tetap dipertahankan aktif (schema tetap dipakai Flask)

---

## 4. Urutan Implementasi (10 Step)

### Step 1 — Foundation Flask
1. Update `requirements.txt` + install ke `.venv`
2. `app/config.py`, `app/extensions.py`, `app/__init__.py` (app factory)
3. Update `Dockerfile`, `docker-compose.yml`, `.env.example`, `Makefile`

### Step 2 — Adaptasi Models (Flask-SQLAlchemy)
1. `db = SQLAlchemy()` di `extensions.py`, `db.init_app(app)` di factory
2. `app/models.py` → `db.Model` + model `User` BARU (tabel `users`); state machine status jadi method model (`mark_done()`, dst.)
3. Migrasi Alembic BARU: create table `users` (satu-satunya perubahan skema; 5 tabel lain tetap)

### Step 3 — Auth + Session
1. `utils/decorators.py` — `login_required` dengan `@wraps(f)`
2. `services/auth_service.py` — verifikasi kredensial via model `User` (bcrypt)
3. CLI seed user: `flask create-user` (default dari env `APP_USERNAME`/`APP_PASSWORD`)
4. `forms/auth_forms.py` + `controllers/auth_controller.py` (GET/POST `/login`, `/logout`; PRG pattern)
5. `templates/base.html` + `templates/auth/login.html`
6. Session config: `SESSION_COOKIE_HTTPONLY=True`, `SESSION_COOKIE_SAMESITE="Lax"`, `PERMANENT_SESSION_LIFETIME`

### Step 4 — Dashboard View (Mock)
1. `controllers/main_controller.py` — route `/` (dashboard, `@login_required`)
2. `templates/dashboard/index.html` — stats cards + project grid placeholder (ikon Font Awesome)
3. `static/css/style.css` — token warna DESIGN.md di atas Tailwind CDN
4. `static/js/app.js` — DOM ready gate + init

### Step 5 — Project Management (Mock)
1. `services/project_service.py` — CRUD + archive (return mock/null dulu)
2. `forms/project_forms.py`
3. Templates: `project/{list,detail,create,edit}.html`

### Step 6 — Task Management (Mock)
1. `services/task_service.py` — CRUD + `toggle_complete()` (delegasi method model)
2. `controllers/task_controller.py` + `forms/task_forms.py`
3. Templates: `task/{list,detail,create,edit}.html` — task tanpa project = "Inbox"

### Step 7 — Component Templates
1. `components/{badge,card,form,modal,navbar}.html` — macro parameter eksplisit
2. `utils/filters.py` + register di app factory

### Step 8 — JavaScript Modules
1. `modal.js` (pattern lengkap: overlay, Escape, scroll lock)
2. `form.js` (loading state, AJAX + CSRF header — mock response dulu)
3. `dashboard.js`

### Step 9 — Disable Notifikasi/Scheduler
1. Pindahkan file FastAPI & services lama ke `archive/` (lihat §3)
2. Header comment `# ARCHIVED 2026-08-27: referensi history — jangan diimport`

### Step 10 — Verify
1. MySQL via Docker (`docker compose up -d mysql`), `alembic upgrade head`, `flask create-user`
2. `.venv` lokal: `flask run` (port 5000) → login → dashboard → semua page render dengan mock
3. Verifikasi visual via browser + lint bila tersedia

Catatan eksekusi: Dockerfile & app service di-compose **ditunda ke fase deployment** (keputusan #14) — `docker-compose.yml` untuk sekarang hanya berisi service MySQL.

---

## 5. Pertanyaan → Jawaban (Semua Terkonfirmasi)

| # | Pertanyaan | Jawaban (Final) |
|---|-----------|-----------------|
| P1 | Port: ganti 8000 → 5000 (default Flask)? | **Ya, port 5000** |
| P2 | Auth tetap env-based tanpa tabel `users`? | **Tidak — pakai model DB, tambah tabel `users`** (mudah nambah user ke depannya; fitur tambah user dilupakan dulu) |
| P3 | Session storage: cookie signed (Flask default) vs server-side? | **Cookie signed** |
| P4 | Mock data: kosong semua vs placeholder? | **Placeholder — berikan beberapa mock data** |
| P5 | Tailwind via CDN vs build step (npm)? | **Tailwind via CDN + ikon SEMUA pakai Font Awesome v6 via CDNJS (emoji sebagai ikon DILARANG)** |
| P6 | Kode lama dipindah ke `archive/` vs rename `_disabled.py`? | **Pindah ke `archive/`** — struktur kerja rapi & bersih |
| P7 | Iterasi lokal (venv) dulu vs langsung Docker? | **Venv dulu; Docker hanya untuk MySQL**; Dockerfile/app container di akhir saat aplikasi jadi |

Catatan tambahan: **styling frontend tetap mengikuti `DESIGN.md`** (Inter, token warna, badges, cards, pills, dsb.).

---

## 6. Roadmap Phases & Detail Todo

> Status legend: ✅ selesai · ⏳ belum · 🔁 berulang per iteration
> Urutan eksekusi disarankan: Phase 2 → Testing (dalam Phase 2) → Phase 3 → Phase 4 → Phase 5.

### Phase 1 — View-First Flask ✅ SELESAI (2026-08-27)

Detail hasil ada di §7. Tidak ada todo tersisa.

---

### Phase 2 — Connect Real DB ✅ SELESAI (2026-08-27)

| # | Todo | Status |
|---|------|--------|
| 2.1 | Load rule `02-model.md` + `17-performance.md` sebelum menulis kode | ✅ (+ `15-testing.md` untuk test suite) |
| 2.2 | `ProjectService`: ganti mock → ORM | ✅ CRUD + validasi ValueError + `count_all()` aggregate |
| 2.3 | `TaskService`: ganti mock → ORM | ✅ filter + sort (done di bawah), toggle via state machine model |
| 2.4 | `TaskService.get_stats` → SQL aggregate | ✅ 3 count query terpisah + `count_all` project (1 query) |
| 2.5 | Re-implement sync Day-H reminder | ✅ `_sync_day_h_reminder()` di task_service (create/update/delete) |
| 2.6 | Choices & filter options dari DB | ✅ `project_choices()` + `get_all()` kini query ORM |
| 2.7 | Edit form prefill dari data DB | ✅ Prefill eksplisit via DTO (string value) |
| 2.8 | Hapus mock builder | ✅ Dipindah ke `archive/mock_services/` |
| 2.9 | Anti N+1 | ✅ Counts via aggregate query (LEFT JOIN + GROUP BY); task list `joinedload(Task.project)` |
| 2.10 | Test suite pytest | ✅ 40 test / 40 pass — auth (8), projects (11), tasks (14), stats (3); conftest SQLite in-memory |
| 2.11 | Verifikasi E2E manual | ✅ Via browser: create project → create task + deadline → row MySQL benar (enum names HIGH/TODO) → Day-H reminder otomatis → toggle complete → completed_at terisi; 404 handler OK |

Catatan teknis Phase 2:
- Model `Task` dapat `apply_status()` (state machine jaga `completed_at`); `mark_done/reopen/toggle_complete` deleget ke sana (02-model.md #3).
- `_utcnow()` helper naive-UTC menggantikan `datetime.utcnow()` yang deprecated.
- Logika tampilan deadline (state/label/stats overdue) memakai `datetime.now()` lokal agar konsisten dengan input form; unifikasi timezone penuh menyusul Phase 4.
- Perintah: `make test` belum ada — jalankan `.venv/bin/python -m pytest -v` (target Makefile menyusul bersama Phase 5).

---

### Phase 3 — Frontend Polish ✅ SELESAI (2026-08-27)

> Goal: rapikan pengalaman visual & interaksi. Sebagian besar sudah tercakup Phase 1 (tokens DESIGN.md, badges, cards, responsive, modal, FAB); ini sisa gap-nya.

| # | Todo | Status | Hasil |
|---|------|--------|-------|
| 3.1 | Skeleton loading state | ✅ | `<template data-skeleton-template>` di task list; `form.js` mengganti daftar dengan skeleton rows saat filter dikirim (clone 3–8 baris, rule #5 12-ajax-js.md) |
| 3.2 | Toast untuk aksi cepat (toggle complete) tanpa reload penuh | ✅ | Diputuskan: **AJAX + update in-place**. `task.js` fetch POST + CSRF header → controller balas JSON saat `X-Requested-With: fetch` (fallback PRG tetap ada tanpa JS); update baris via class toggle + toast `role="status"` |
| 3.3 | Decide dark mode | ✅ | Diputuskan: **skip dulu** — token didefinisikan nanti di DESIGN.md saat ada kebutuhan nyata (catatan di Known Gaps) |
| 3.4 | Keyboard shortcuts | ✅ | `shortcuts.js`: `n` = tugas baru, `/` = fokus filter (guard: diabaikan saat mengetik / ada modifier); spesifikasi ditambahkan ke DESIGN.md |
| 3.5 | Calendar view (optional) | ✅ | Diputuskan: **tunda** — nilai kebutuhan rendah (catatan di Known Gaps DESIGN.md) |
| 3.6 | Aksesibilitas audit | ✅ | Kontras token di-tuning (steel/stone diredamkan; badge/alert pakai varian `*-ink` — semua ≥4.5:1); filter select dapat `aria-label`; modal dapat fokus management (fokus masuk, trap Tab, restore ke pemicu); meta description + favicon SVG. Lighthouse a11y **100** (desktop & mobile) |
| 3.7 | Responsive audit mobile | ✅ | Bottom nav + FAB 56px + grid 1 kolom + tanpa overflow terverifikasi di 375×667; modal kini **full-screen di mobile** (`h-dvh` rounded-none) / centered panel di desktop — sesuai DESIGN.md |
| 3.8 | Evaluasi Alpine.js/HTMX bila form makin kompleks | ✅ | Diputuskan: **tidak perlu sekarang** — form masih sederhana, vanilla JS cukup (exception clause dievaluasi ulang bila form makin kompleks) |

Catatan teknis Phase 3:
- Update in-place toggle digerakkan class CSS (`is-done`/`is-loading` di style.css) — bukan manipulasi inline style (rule #3 12-ajax-js.md). Peta badge status di `task.js` HARUS sinkron dengan macro `status_badge` badge.html.
- Angka stats di dashboard tidak disinkronkan live setelah toggle (refresh pada load berikutnya) — kesadaran aksi disampaikan toast.
- Copy "(Simulasi)" sisa fase mock dihapus dari modal delete (delete sudah real sejak Phase 2).
- Lighthouse: a11y/best-practices/SEO 100 di dashboard (desktop), task detail & task list (mobile).

---

### Phase 4 — Notifikasi & Scheduler ⏳

> Goal: rebuild fitur notifikasi dengan memperbaiki bug lama (lihat `archive/README.md` — JANGAN copy mentah). Reminder section di task detail diaktifkan.

| # | Todo | Catatan |
|---|------|---------|
| 4.1 | Load rule `03-service.md` ulang + review bug list `archive/README.md` | 5 bug diketahui |
| 4.2 | Pilih arsitektur scheduler di Flask | Background thread APScheduler vs proses cron terpisah — pertimbangkan gunicorn multi-worker (duplikat job!) |
| 4.3 | Rebuild reminder checker | day_h / relative / absolute — adaptasi `archive/scheduler_disabled.py` |
| 4.4 | Fix forwarding `endpoint_url` + `headers` di pengiriman | Bug utama versi lama |
| 4.5 | Template pesan: placeholder `{priority}`/`{status}`/`{reminder_type}` pakai nilai asli | Bug versi lama |
| 4.6 | Retry real + update `retry_count` | `retry_notification` lama tidak pernah dipanggil |
| 4.7 | Konsistensi timezone | Pilih satu (UTC atau local), dokumentasikan |
| 4.8 | Fix race: kirim dulu → baru `sent=True` dalam 1 transaksi commit | Bug versi lama |
| 4.9 | Halaman Settings: webhook config + tombol test + template editor | Blueprint `setting_bp` baru |
| 4.10 | Halaman log notifikasi (filter status/task, pagination) | Reuse komponen badge/card |
| 4.11 | UI reminder per task (create/list/delete) di task detail | Aktifkan section yang sekarang placeholder |
| 4.12 | Testing dengan mock endpoint (httpbin / webhook.site) lalu WAHA asli | — |

---

### Phase 5 — Deployment Docker ⏳

> Goal: aplikasi jalan di Docker production-ready. Ditunda sampai fitur inti stabil (keputusan #14).

| # | Todo | Catatan |
|---|------|---------|
| 5.1 | Update `Dockerfile` | CMD gunicorn `app:create_app()`, non-root user |
| 5.2 | `docker-compose.yml`: tambah kembali service aplikasi | Port 5000, depends_on mysql healthy |
| 5.3 | `.env.production` + SECRET_KEY kuat (`openssl rand -hex 32`) | — |
| 5.4 | Hardening: `SESSION_COOKIE_SECURE=True` (HTTPS-only), secure headers via `after_request` | Checklist `16-security.md` |
| 5.5 | Rate limiting login (`flask-limiter`) + account lockout sederhana | Checklist `16-security.md` |
| 5.6 | Migrasi otomatis saat start container (entrypoint) atau manual `make migrate-up` | Putuskan strategi |
| 5.7 | Backup MySQL terjadwal + dokumentasi restore | mysqldump cron |
| 5.8 | HTTPS (reverse proxy Caddy/nginx) + monitoring dasar | Optional sesuai kebutuhan |
| 5.9 | Update README + GETTING_STARTED sesuai realita Flask | README masih versi FastAPI |

---

### Future — FastAPI (Mobile API) 📝 CATATAN SAJA

> Tidak direncanakan sekarang (keputusan #1). Baru dievaluasi saat aplikasi mobile mulai dibangun. Saran arsip: endpoint terpisah `api/` versi Flask (blueprint) bisa jadi batu loncatan tanpa framework baru.

### Catatan Dokumen Lain yang Perlu Diperbarui 🔁

| Dokumen | Aksi | Kapan |
|---|---|---|
| `CONCEPT.md` | Tech stack & struktur masih FastAPI — update ke Flask | Saat Phase 2 mulai |
| `PROJECT_TRACKER.md` | Masih tracker versi lama (5 phase FastAPI complete) — ganti dengan referensi ke roadmap doc ini | Saat Phase 2 mulai |
| `README.md` / `GETTING_STARTED.md` | Masih instruksi uvicorn/FastAPI | Phase 5 |
| `DESIGN.md` | Tambah token dark mode / shortcut bila diputuskan di Phase 3 | Phase 3 ✅ — shortcut + toast + tuning AA ditambahkan; dark mode & calendar ditunda |

---

**Dibuat:** 2026-08-27
**Status:** ✅ Phase 1 & 2 & 3 SELESAI — hasil eksekusi: §7 (Phase 1), catatan Phase 2 di §6, §8 (Phase 3).

---

## 7. Hasil Eksekusi Phase 1 (2026-08-27)

| Step | Status | Bukti |
|------|--------|-------|
| 1. Foundation Flask | ✅ | App factory + config + extensions + requirements (Flask 3.0.3) ter-install di `.venv` |
| 2. Models + `users` | ✅ | Migrasi `b3f8c1a5d9e2` jalan; tabel `users` dibuat; seed `admin` via `flask create-user` |
| 3. Auth + session | ✅ | Login bcrypt via DB → session cookie; `/` redirect 302 ke `/auth/login` bila belum login |
| 4. Dashboard mock | ✅ | Stats 4 kartu + project grid + tugas terbaru + FAB mobile render |
| 5. Project mock | ✅ | List/detail/create/edit + archive/delete (simulasi) + modal konfirmasi |
| 6. Task mock | ✅ | List + filter (project/status/priority, autosubmit) + detail + create/edit + toggle |
| 7. Components | ✅ | `badge/card/form/modal/navbar/bottom_nav` macro — ikon semua Font Awesome v6 (CDNJS), tanpa emoji |
| 8. JS modules | ✅ | `modal/form/dashboard/app` IIFE strict-mode; behavior via `data-*`; flash auto-dismiss 4s |
| 9. Disable notifikasi | ✅ | Semua kode FastAPI lama di `archive/` (+README); reminder section di task detail = placeholder disabled |
| 10. Verify | ✅ | MySQL Docker healthy; `/health` ok; PRG + flash "Simulasi: ..." terkonfirmasi via curl; console browser bersih (hanya warning Tailwind CDN yang memang expected) |

**Cara jalankan**: `make mysql-up && make migrate-up && make seed-user && make dev` → http://localhost:5000 (admin/changeme)

---

## 8. Hasil Eksekusi Phase 3 (2026-08-27)

| Item | Bukti verifikasi |
|------|------------------|
| 3.1 Skeleton | Dispatch submit filter → 28 blok skeleton ter-render, 0 baris task tersisa (DOM check) |
| 3.2 Toggle AJAX | Klik check di dashboard → row `is-done`, badge "Selesai", aria-label & icon swap, toast muncul, URL tetap `/` (tanpa reload); reopen balik normal |
| 3.2 Fallback | Tanpa JS: POST biasa → 302 PRG + flash (test `test_complete_tanpa_xhr_tetap_redirect_prg`) |
| 3.2 Kontrak JSON | `X-Requested-With: fetch` → `{status:"ok", data:{...}, message}` / 404 `{status:"error"}` (3 test baru; total 43/43 pass) |
| 3.4 Shortcuts | `n` → navigasi ke `/tasks/create`; saat fokus di input judul `n` mengetik (guard OK); `/` → fokus select `project_id` |
| 3.6 A11y | Lighthouse a11y 100 (dashboard desktop; task detail & task list mobile); kontras semua pasangan token teks ≥4.5:1 (dihitung, bukan tebak) |
| 3.6 Modal a11y | Fokus masuk modal saat open, Tab trap tersiklus, Escape tutup + fokus kembali ke tombol pemicu |
| 3.7 Mobile 375×667 | Bottom nav 61px + `pb-24` main; FAB 56×56 di atas nav; grid 1 kolom; 0px horizontal overflow; modal full-screen (375×667, rounded 0) |
| Bonus | Favicon SVG inline (404 hilang), meta description, hapus copy "(Simulasi)" sisa fase mock |
