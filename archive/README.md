# archive/ — Kode Lama (Referensi History)

> Dipindahkan: 2026-08-27, saat migrasi FastAPI → Flask.
> Status: **DISABLE — jangan di-import.** Tidak ada kode Flask baru yang boleh mereferensi folder ini.
> Alasan dipertahankan: referensi history implementasi sebelumnya (lihat `docs/2026-08-27 - Rencana Migrasi Flask.md` §0 keputusan #5 & #13). Hapus nanti jika sudah benar-benar tidak dibutuhkan.

## Isi

| File/Folder | Asal | Keterangan |
|---|---|---|
| `fastapi_main.py` | `app/main.py` | Entry point FastAPI + lifespan scheduler |
| `fastapi_config.py` | `app/config.py` | Pydantic Settings (env-based) |
| `fastapi_database.py` | `app/database.py` | Engine SQLAlchemy + `get_db` generator |
| `fastapi_schemas.py` | `app/schemas.py` | Pydantic request/response schemas |
| `fastapi_security.py` | `app/security.py` | Token HMAC-SHA256 buatan + bcrypt verify |
| `fastapi_api/` | `app/api/` | Routes (auth, projects, tasks, reminders, webhooks, stats) + dependencies |
| `scheduler_disabled.py` | `app/services/scheduler.py` | APScheduler pengecek deadline (tiap 1 menit) |
| `webhook_disabled.py` | `app/services/webhook.py` | Pengirim webhook (WAHA) + retry backoff |
| `notification_disabled.py` | `app/services/notification.py` | Render template pesan notifikasi |
| `static_legacy/` | `app/static/` | Frontend SPA vanilla lama (index.html, js, css) |

## Bug yang Sudah Diketahui (jangan copy begitu saja)

1. `scheduler_disabled.py` → `process_reminder()` tidak meneruskan `endpoint_url`/`headers` ke `send_webhook` → notifikasi nyata gagal "No webhook URL configured".
2. `fastapi_api/dependencies.py` → `get_db` dengan `lru_cache` session (berbahaya, dead code — routes memakai `app.database.get_db`).
3. `notification_disabled.py` → placeholder `{priority}`/`{status}`/`{reminder_type}` diisi hardcoded.
4. Retry mechanism (`retry_notification`) tidak pernah dipanggil scheduler; `retry_count` selalu 0.
5. Timezone campur: `datetime.now()` (lokal) vs `datetime.utcnow()`.

Detail lengkap: `docs/2026-08-27 - Backend & Database Analysis.md` §7.
