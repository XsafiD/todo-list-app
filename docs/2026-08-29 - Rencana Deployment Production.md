# Rencana Deployment Production — Dashboardku

> **Tanggal**: 2026-08-29
> **Status**: Hasil riset & rekomendasi (pre-implementasi Phase 5)
> **Referensi rule**: `docs/coding-standards/coding-rules/18-deployment.md`
>
> ⚠️ **Update 2026-08-31**: mekanisme seed user (`flask create-user` / env
> `APP_USERNAME`/`APP_PASSWORD`/`APP_PASSWORD_HASH`) **sudah dihapus**. Akun
> pertama sekarang dibuat via halaman setup awal di browser (`/auth/setup`,
> aktif hanya saat tabel `users` kosong, setelah itu 404 permanen). Bagian di
> bawah yang menyebut seed/create-user berlaku untuk versi sebelum update.

---

## 1. Ringkasan Eksekutif

Dashboardku akan dideploy ke **home server Ubuntu Server 24.04** yang sudah menjalankan Docker, Tailscale, dan cloudflared (domain di Cloudflare). Rekomendasi: **Docker Compose 2 service** (`app` gunicorn + `mysql`), tanpa container reverse proxy tambahan — HTTPS & akses sudah ditangani Cloudflare (jalur utama) dan Tailscale (jalur cadangan).

Deploy manual via SSH: `git pull` → `up -d --build` → `alembic upgrade head`.

---

## 2. Hasil Riset Kondisi Existing

### 2.1 Temuan di repo

| # | Temuan | Dampak ke Production |
|---|--------|----------------------|
| 1 | `Dockerfile` **stale** — masih era FastAPI (`uvicorn app.main:app --reload`, modul sudah dihapus ke `archive/`) | WAJIB rewrite total; `--reload` juga dilarang di production (rule 18) |
| 2 | `docker-compose.yml` hanya berisi MySQL (sesuai keputusan migrasi #14) | Perlu file compose terpisah untuk production |
| 3 | **APScheduler jalan di dalam proses web** (`app/scheduler.py`, job auto-archive 23:59) | Gunicorn multi-worker → job dieksekusi **dobel**. Guard saat ini hanya untuk Werkzeug reloader |
| 4 | `requirements.txt` belum ada WSGI server (gunicorn) | Perlu ditambah |
| 5 | Belum ada `ProxyFix` di app factory | Di belakang cloudflared/tailscale-serve, `request.remote_addr` jadi IP proxy — log tidak akurat |
| 6 | `/health` sudah ada (`app/controllers/main_controller.py:37`), public, tanpa query DB | ✅ Siap dipakai sebagai container healthcheck (rule 18 #3) |
| 7 | `.env.production` sudah ada sketsanya dan **sudah ter-gitignore** (`.gitignore:59`) | Perlu dilengkapi variabel production (DB prod, hash password, `SESSION_COOKIE_SECURE`) |
| 8 | Tailwind + Font Awesome via CDN | Berfungsi, tapi client butuh internet & ada warning console CDN — opsional diprecompile |
| 9 | `docs/TESTING_DEPLOYMENT.md` sebagian besar masih era FastAPI/uvicorn | Out of scope dokumen ini; bisa dirapikan menyusul |

### 2.1 Kondisi infrastruktur user (home server)

- Ubuntu Server 24.04 + Docker terpasang ✅
- Tailscale aktif — akses SSH & jalur cadangan
- cloudflared (Zero Trust) aktif + domain di Cloudflare — HTTPS di edge, tanpa perlu buka port inbound router
- Deploy: manual SSH, database: tetap MySQL

---

## 3. Opsi yang Dipertimbangkan

| Opsi | Skema | Kelebihan | Kekurangan | Verdict |
|------|-------|-----------|------------|---------|
| **A. Docker Compose di home server** | `app` + `mysql` container, cloudflared → localhost | Reproducible, mudah dipindah/restore, sesuai rule 18, zero cost | Perlu kelola image & volume | ✅ **DIPILIH** |
| B. Bare metal (systemd + gunicorn + nginx + MySQL apt) | Tanpa Docker untuk app | Hemat resource sedikit | Setup manual, rawan drift antar reinstall, backup/restore lebih ribet | ❌ |
| C. PaaS (Railway/Render/Fly) | Managed | Zero-ops | Berbayar, MySQL tidak semua support, scheduler-in-web-process bermasalah di platform yang scale/restart instance | ❌ |
| D. K8s / Swarm | Orchestration penuh | Overkill total untuk single-user app | Kompleksitas tidak sebanding | ❌ |

**Kenapa A**: infrastruktur user sudah 90% siap (Docker + cloudflared + Tailscale), aplikasi single-user sehingga tidak butuh orchestration, dan rule `18-deployment.md` memang menargetkan pola Docker + gunicorn.

---

## 4. Arsitektur Target

```
                    ┌─────────────────────────────────────┐
 Internet ──HTTPS──▶│ Cloudflare (domain, TLS termination)│  ← jalur utama
                    │ + Access policy (Zero Trust)        │
                    └──────────────┬──────────────────────┘
                                   │ tunnel terenkripsi
                          cloudflared (sudah ada, host)
                                   │ http://localhost:5000
 ┌─ Docker Compose (prod) ────────▼─────────────────────────────┐
 │  app       gunicorn Flask :5000   (publish 127.0.0.1 saja)   │
 │  mysql     MySQL 8.0               (TANPA published port)    │
 │              └─ volume mysql_prod_data                        │
 └───────────────────────────────────────────────────────────────┘
                                   ▲
 Tailnet ──HTTPS── tailscale serve ┘  ← jalur cadangan (tunnel down / tanpa internet)

 Backup: cron harian mysqldump → ./backups/ (keep 7 hari)
```

**Prinsip expose:**

- `app` hanya publish di `127.0.0.1:5000` — tidak tersentuh LAN/publik.
- Jalur cadangan Tailscale memakai **`tailscale serve`** (proxy tailnet → `localhost:5000`, dapat HTTPS + hostname MagicDNS otomatis) — tanpa perlu publish port ke IP 100.x. Alternatif: publish `100.x.y.z:5000:5000` di compose, tapi IP Tailscale harus di-hardcode dan ganti komposisinya bila mesin ganti tailnet.
- `mysql` tidak publish port sama sekali; akses admin via `docker compose exec`.

---

## 5. Detail Skema per Komponen

### 5.1 Dockerfile (rewrite)

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1
# FLASK_DEBUG/DEBUG TIDAK di image — via compose env_file (default false)

WORKDIR /app

# pymysql & bcrypt pure-python/wheel — TIDAK perlu gcc/libmysqlclient
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN addgroup --system app && adduser --system --ingroup app app \
    && chown -R app:app /app
USER app

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request;urllib.request.urlopen('http://localhost:5000/health', timeout=3)"

CMD ["gunicorn", "--bind", "0.0.0.0:5000", \
     "--workers", "1", "--threads", "4", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "app:create_app()"]
```

Catatan penting:

- **`--workers 1 --threads 4`** — keputusan kunci (lihat §5.4). Single-user, throughput bukan isu; blocking di I/O DB tertangani threads.
- `HEALTHCHECK` di image + healthcheck di compose (rule 18 #2) — dobel tidak masalah, compose yang dipakai `depends_on`.
- Non-root user `app` (rule 18 #6, DILARANG container root).

### 5.2 docker-compose.prod.yml (baru, self-contained)

```yaml
# Production stack — dipakai dengan: docker compose -f docker-compose.prod.yml up -d
# Dev tetap pakai docker-compose.yml (MySQL saja) — jangan dicampur.
services:
  app:
    build: .
    container_name: dashboardku-app
    env_file: .env.production
    environment:
      - SCHEDULER_ENABLED=true
      - DB_HOST=mysql          # override .env.production (hostname internal docker)
      - DB_PORT=3306
    ports:
      - "127.0.0.1:5000:5000"   # HANYA loopback — cloudflared & tailscale serve yang expose
    restart: unless-stopped
    depends_on:
      mysql:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request;urllib.request.urlopen('http://localhost:5000/health', timeout=3)"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 30s
    deploy:
      resources:
        limits:
          memory: 512M

  mysql:
    image: mysql:8.0
    container_name: dashboardku-mysql-prod
    environment:
      - MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
      - MYSQL_DATABASE=${DB_NAME}
      - MYSQL_USER=${DB_USER}
      - MYSQL_PASSWORD=${DB_PASS}
    command: --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
    volumes:
      - mysql_prod_data:/var/lib/mysql
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-p${MYSQL_ROOT_PASSWORD}"]
      interval: 5s
      timeout: 5s
      retries: 10

volumes:
  mysql_prod_data:
```

Poin desain:

- File **self-contained** (bukan override dari `docker-compose.yml`) supaya dev & prod tidak saling bocor config.
- Kredensial DB via `.env.production` (compose otomatis membaca file ini untuk interpolasi `${...}`) — tidak ada password hardcoded (rule 18 DILARANG #2).
- `DB_HOST=mysql` di-override via `environment` agar `.env.production` tetap bisa menyimpan nilai lain untuk tooling manual.
- Volume terpisah `mysql_prod_data` ≠ `mysql_data` (dev) — tidak akan tertimpa.
- `deploy.resources` di compose non-Swarm berfungsi sebagai limit memory (didukung `docker compose` v2).

### 5.3 Strategi env & secrets

File: `.env.production` di server (gitignored, `chmod 600`). Isi:

```env
# Database (DB_HOST dioverride compose ke 'mysql')
DB_NAME=dashboardku_prod
DB_USER=dashboardku_user
DB_PASS=<password-kuat-random>
MYSQL_ROOT_PASSWORD=<root-password-kuat-random>

# Flask
SECRET_KEY=<openssl rand -hex 32>
DEBUG=false

# Auth seed (flask create-user) — OBSOLETE 2026-08-31: akun pertama sekarang dibuat via browser (/auth/setup)
# APP_USERNAME=admin
# APP_PASSWORD_HASH=<bcrypt hash — generate sekali, taruh literal, bukan $(...)>

# Hardening session
SESSION_COOKIE_SECURE=true
```

Generate:

```bash
openssl rand -hex 32                                                          # SECRET_KEY
python3 -c "import bcrypt; print(bcrypt.hashpw(b'password_kuat'.encode(), bcrypt.gensalt()).decode())"   # APP_PASSWORD_HASH
```

⚠️ Catatan: nilai `$(...)` di `.env` **tidak diekspansi** oleh docker compose / python-dotenv — harus literal hasil generate, bukan template command.

⚠️ Catatan (temuan uji 2026-08-30): `$` di nilai env_file **di-interpolasi** docker compose — hash bcrypt (`$2b$12$...`) WAJIB ditulis dengan escaping `$$` di `.env.production` (`$$2b$$12$$...`), kalau tidak hash terpotong diam-diam dan login selalu gagal. Alternatif: seed interaktif `docker compose -f docker-compose.prod.yml exec -it app flask create-user -p "password"` tanpa menyimpan hash di env.

### 5.4 Scheduler di production (analisis krusial)

`app/scheduler.py` menjalankan `BackgroundScheduler` **di dalam proses web**. Di dev aman karena ada guard Werkzeug reloader. Di production dengan gunicorn:

| Konfigurasi | Risiko | Keterangan |
|-------------|--------|------------|
| `--workers 4` | ❌ Job dobel | 4 proses fork → 4 scheduler → auto-archive 4x, log count salah, race DB |
| `--workers 1 --threads 4` | ✅ Aman | Tepat 1 scheduler; threads cukup untuk traffic single-user |
| Scheduler pisah container (`SCHEDULER_ENABLED=true` hanya di situ) | ✅ Aman + scalable | Overkill untuk sekarang; jadi opsi bila app perlu multi-worker |

**Keputusan**: `--workers 1 --threads 4`. `SCHEDULER_ENABLED` sudah env-driven (`app/config.py:47`) jadi opsi split tetap terbuka tanpa refactor.

Timezone: job cron pakai **waktu lokal container**. Base image `python:3.12-slim` default UTC → job 23:59 akan jalan 23:59 UTC (06:59 WIB), salah! **Solusi**: set `TZ=Asia/Jakarta` di `environment` app container (glibc di Debian slim membaca `TZ` langsung, tanpa apt tambahan) — konsisten konvensi deadline lokal.

### 5.5 ProxyFix (perubahan kode kecil)

`app/__init__.py`, setelah `app = Flask(__name__)`:

```python
from werkzeug.middleware.proxy_fix import ProxyFix

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)
```

Rantai proxy tepat 1 hop (cloudflared **atau** tailscale serve), jadi `x_for=1, x_proto=1` — sesuai rule 18 #7. Tanpa ini, semua request tercatat berasal dari `127.0.0.1`.

### 5.6 Cloudflared (jalur utama — konfigurasi di server, sudah terpasang)

Tambah ingress di config cloudflared existing (`config.yml`):

```yaml
ingress:
  - hostname: dashboard.domain-anda.com
    service: http://localhost:5000
    originRequest:
      noTLSVerify: true          # origin http biasa; TLS dihentikan di edge
      connectTimeout: 30s
  # ... rule lain yang sudah ada ...
  - service: http_status:404
```

Lalu DNS CNAME otomatis: `cloudflared tunnel route dns <tunnel> dashboard.domain-anda.com`.

**Rekomendasi Zero Trust**: pasang **Cloudflare Access** policy di hostname tersebut (mis. require email OTP akunmu). Efeknya: sebelum sampai login Dashboardku, pengunjung harus lewat auth Cloudflare dulu — double auth untuk aplikasi pribadi. Bot/scanner tidak akan pernah menyentuh form login.

### 5.7 Tailscale serve (jalur cadangan)

Di server:

```bash
tailscale serve --bg http://localhost:5000
```

Hasil: `https://dashboardku.<tailnet>.ts.net` aktif di seluruh tailnet dengan sertifikat otomatis. Tanpa port terbuka, tanpa config tambahan. Cocok saat tunnel Cloudflare down atau ingin akses offline-internet.

### 5.8 Backup & restore

`scripts/backup_db.sh` (di host, dijalankan cron):

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p backups
docker compose -f docker-compose.prod.yml exec -T mysql \
  mysqldump -u root -p"$MYSQL_ROOT_PASSWORD" --single-transaction \
  --routines --triggers "$DB_NAME" | gzip > "backups/db-$(date +%F).sql.gz"
# keep 7 hari
ls -1t backups/db-*.sql.gz | tail -n +8 | xargs -r rm --
```

Cron root (baca env dari `.env.production`):

```
0 4 * * * cd /opt/dashboardku && bash -c 'set -a; source .env.production; set +a; ./scripts/backup_db.sh' >> backups/backup.log 2>&1
```

Restore:

```bash
gunzip -c backups/db-2026-08-29.sql.gz | \
  docker compose -f docker-compose.prod.yml exec -T mysql mysql -u root -p"$MYSQL_ROOT_PASSWORD" "$DB_NAME"
```

**Restore uji coba minimal 1x** sebelum dinyatakan production (backup yang belum pernah direstore = bukan backup).

---

## 6. Runbook Deploy

### 6.1 First deploy (sekali)

```bash
# 1. Clone ke server (via SSH/Tailscale)
sudo mkdir -p /opt/dashboardku && sudo chown $USER /opt/dashboardku
git clone <repo-url> /opt/dashboardku && cd /opt/dashboardku

# 2. Siapkan .env.production (lihat §5.3) + chmod 600
cp .env.production.example .env.production && $EDITOR .env.production && chmod 600 .env.production
openssl rand -hex 32   # isi SECRET_KEY

# 3. Naikkan stack
docker compose -f docker-compose.prod.yml up -d --build

# 4. Migrasi (alembic sudah jalan otomatis di entrypoint; ini opsional / cek)
docker compose -f docker-compose.prod.yml exec app alembic current

# 5. Setup awal — buka browser http://<server>:5000 (sebelum expose ke publik), buat akun pertama (hanya sekali)

# 6. Expose
#    a. cloudflared ingress (§5.6) lalu restart cloudflared
#    b. tailscale serve --bg http://localhost:5000   (§5.7)

# 7. Verifikasi
curl -s http://localhost:5000/health
# → login via domain, buat project + task, cek scheduler:
docker compose -f docker-compose.prod.yml logs app | grep -i scheduler
```

### 6.2 Proses update (lokal → server)

**Siklus lengkap setiap ada perubahan:**

**Di lokal (mesin dev):**

```bash
# 1. Kerjakan fitur/fix di branch, lalu test
.venv/bin/python -m pytest

# 2. REVIEW file migration bila ada yang baru (autogenerate bisa menghasilkan
#    drop_table/drop_column yang destruktif — pastikan memang disengaja)
git status && git diff

# 3. Commit & push
git add -p && git commit -m "..." && git push
```

**Di server (via SSH/Tailscale):**

```bash
cd /opt/dashboardku

# 1. Backup dulu (net keselamatan sebelum menyentuh apapun)
./scripts/backup_db.sh

# 2. Tarik kode terbaru
git pull

# 3. Rebuild image + recreate container (data MySQL tidak tersentuh — lihat §6.3)
docker compose -f docker-compose.prod.yml up -d --build

# 4. Apply migration skema baru (aditif — baris data tidak diubah)
docker compose -f docker-compose.prod.yml exec app alembic upgrade head

# 5. Verifikasi
docker compose -f docker-compose.prod.yml ps                # keduanya healthy
curl -s http://localhost:5000/health
docker compose -f docker-compose.prod.yml logs app --tail 50 # tidak ada error
# → login via domain, smoke test ringan (buka dashboard, buat/hapus task)
```

Downtime ≈ beberapa detik (container restart) — acceptable untuk single-user. Bisa dibungkus `make deploy` di server (backlog §8 item 9).

**Rollback bila update bermasalah:**

```bash
# Kode kembali ke commit terakhir yang sehat
git log --oneline -5                  # cari hash yang baik
git checkout <hash-yang-baik>
docker compose -f docker-compose.prod.yml up -d --build

# Bila migration perlu di-rollback (HANYA bila yakin — downgrade bisa destruktif):
docker compose -f docker-compose.prod.yml exec app alembic downgrade -1

# Bila data harus dipulihkan (kasus terburuk):
gunzip -c backups/db-<tanggal>.sql.gz | \
  docker compose -f docker-compose.prod.yml exec -T mysql mysql -u root -p"$MYSQL_ROOT_PASSWORD" "$DB_NAME"
```

### 6.3 Keamanan data saat update ("data hilang ngga?")

**Tidak — data dan kode terpisah total:**

| Layer | Lokasi | `git pull` / rebuild berpengaruh? |
|-------|--------|------------------------------------|
| Kode + file migration | `/opt/dashboardku` (git) | ✅ Ya — memang itu tujuannya |
| Data MySQL | Docker volume `mysql_prod_data` | ❌ Tidak — volume di luar git & di luar container FS |
| `.env.production`, `backups/` | Folder repo di server (untracked/gitignored) | ❌ Tidak — `git pull` tidak menyentuh file untracked |
| Data dev lokal | Volume `mysql_data` di mesin lokal | ❌ Terpisah total dari prod |

Bahkan `docker compose down` pun volume tetap aman (container dibuang, volume tidak). `alembic upgrade head` hanya mengubah **skema** secara aditif (ALTER/CREATE) — baris data tidak disentuh.

**Perintah yang JUSTRU berbahaya** (jangan pernah di server prod):

| # | Perintah | Efek |
|---|----------|------|
| 1 | `docker compose down -v` / `docker volume rm` | ❌ Hapus volume = **hapus semua data** |
| 2 | `docker system prune --volumes` | ❌ Ikut menghapus volume |
| 3 | `git clean -xfd` | ❌ Hapus `.env.production` + `backups/` |
| 4 | Migration `drop_table`/`drop_column` tanpa review | ❌ Kehilangan kolom/tabel data |
| 5 | Saran "reset database" di `docs/TESTING_DEPLOYMENT.md` (era lama) | ❌ Pola dev-only (`docker volume rm`) — jangan dijalankan di prod |

Net keselamatan final tetap backup harian (§5.8) + step backup manual sebelum update (§6.2 step 1) — selama itu jalan, bahkan kesalahan no. 1 masih bisa dipulihkan.

---

## 7. Checklist Security (production)

Mengacu rule 18 (WAJIB/DILARANG) + rule 16:

- [ ] `DEBUG=false`, tidak ada `flask run`/reloader di production
- [ ] `SECRET_KEY` hasil `openssl rand -hex 32`, hanya di `.env.production` (chmod 600, gitignored ✅ sudah)
- [ ] Akun pertama dibuat via setup awal browser — tidak ada password/hash di env (update 2026-08-31)
- [ ] Container non-root user ✅ (di Dockerfile §5.1)
- [ ] MySQL tanpa published port; kredensial kuat, tidak di git
- [ ] `SESSION_COOKIE_SECURE=true` (HTTPS sudah pasti di kedua jalur akses)
- [ ] Cloudflare Access policy aktif di hostname
- [ ] Backup harian jalan + pernah diuji restore
- [ ] `/health` dipakai container healthcheck (public, tanpa DB ✅ sudah ada)
- [ ] Firewall host: tidak ada port app/mysql terbuka ke LAN/publik (hanya SSH + tailscale0)

---

## 8. Backlog Pekerjaan (implementasi Phase 5)

| # | Item | File | Catatan |
|---|------|------|---------|
| 1 | Rewrite Dockerfile (gunicorn, non-root, healthcheck) | `Dockerfile` | §5.1 |
| 2 | Compose production | `docker-compose.prod.yml` (baru) | §5.2 |
| 3 | Tambah gunicorn | `requirements.txt` | pin versi, mis. `gunicorn==23.0.0` |
| 4 | ProxyFix | `app/__init__.py` | §5.5 |
| 5 | Env `TZ=Asia/Jakarta` + `SESSION_COOKIE_SECURE` | compose + `app/config.py` | §5.4, §5.3 |
| 6 | `.dockerignore` | `.dockerignore` (baru) | exclude `.venv/ .git/ archive/ docs/ tests/ *.log .env* backups/` |
| 7 | Backup script + cron | `scripts/backup_db.sh` (baru) | §5.8 |
| 8 | Template env production | `.env.production.example` (baru, commit) | tanpa nilai rahasia, hanya placeholder |
| 9 | Makefile targets prod | `Makefile` | `deploy`, `prod-up`, `prod-logs`, `backup` |
| 10 | Uji restore backup | runbook | §5.8 |

Konfigurasi **di luar repo** (di server): cloudflared ingress, Cloudflare Access, `tailscale serve`, cron.

## 9. Open Items (opsional, pasca-launch)

1. **Tailwind precompile** — ganti CDN dengan build step (Tailwind CLI) → ringankan load, hilangkan warning CDN, app tetap jalan offline penuh di tailnet.
2. **Rate limiting login** — `Flask-Limiter` (berbasis IP; dengan ProxyFix IP sudah benar). Cloudflare Access sudah jadi lapisan pertama, jadi prioritas rendah.
3. **Monitoring uptime** — Uptime Kuma di home server (opsional, sekalian monitor service lain).
4. **Offsite backup** — sinkron `backups/` ke storage luar (rclone ke cloud / PC lain) menyusul.
5. **Rapikan `docs/TESTING_DEPLOYMENT.md`** — masih berisi instruksi era FastAPI; sampaykan setelah Phase 4 selesai.

---

**Kesimpulan**: skema A (Docker Compose di home server) dengan gunicorn 1-worker, expose via cloudflared (utama) + tailscale serve (cadangan), MySQL internal tanpa port, backup harian teruji. Semua kebutuhan bisa dikerjakan dalam backlog §8 tanpa perubahan arsitektur aplikasi — hanya ProxyFix + config env yang menyentuh kode.
