# Dashboardku - Concept Specification

## 🎯 Overview

Aplikasi todo list custom dengan notifikasi berbasis webhook untuk mengatasi keterbatasan Todoist. Dibangun untuk workflow personal dengan fleksibilitas penuh dalam pengelolaan task dan reminder.

## 📋 Background & Requirements

### Masalah
- Todoist memiliki keterbatasan dalam kustomisasi workflow
- Fitur premium Todoist membatasi akses ke fitur reminder
- Butuh kontrol penuh atas sistem notifikasi

### Solusi
- Aplikasi todo list sendiri bernama "Dashboardku"
- Notifikasi via webhook (seperti Uptime Kuma)
- Integrasi dengan WhatsApp Gateway (WAHA)
- Reminder flexible sesuai kebutuhan workflow

---

## 🚀 MVP Scope

### Fitur Utama
✅ Single user (simple username/password)
✅ Project-based task management
✅ Flexible reminder system (2 hari sebelum, 2 jam sebelum, hari H)
✅ Webhook POST ke WAHA (WhatsApp)

---

## 🛠️ Tech Stack

```
├── Backend: FastAPI (Python 3.11+)
│   ├── Async/await support
│   ├── Auto Swagger UI docs
│   ├── Pydantic validation
│   └── Docker-friendly
│
├── Frontend: Vanilla HTML/JS + CSS
│   ├── Tailwind CSS (via CDN)
│   ├── Alpine.js (optional, untuk reactivity)
│   └── HTMX (optional, untuk dynamic update)
│
├── Database: MySQL 8.0 (Docker)
├── Scheduler: APScheduler (Python)
├── Auth: Simple Basic Auth / API Key
└── Deployment: Docker Compose
```

---

## 📁 Project Structure

```
dashboardku/
├── docker-compose.yml          # MySQL + App service
├── Dockerfile                  # App container
├── requirements.txt            # Python deps
├── .env.example                # Environment variables
│
├── app/
│   ├── main.py                # FastAPI entry point
│   ├── models.py              # SQLAlchemy models
│   ├── schemas.py             # Pydantic schemas
│   ├── database.py            # DB connection
│   │
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py        # Authentication
│   │   │   ├── projects.py    # Project CRUD
│   │   │   ├── tasks.py       # Task CRUD
│   │   │   ├── reminders.py   # Reminder CRUD
│   │   │   └── webhooks.py    # Webhook config
│   │   └── dependencies.py
│   │
│   ├── services/
│   │   ├── scheduler.py       # Deadline checker & notification
│   │   ├── webhook.py         # HTTP POST ke WAHA
│   │   └── notification.py    # Template & logic notifikasi
│   │
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── index.html
│   │
│   └── templates/
│       └── *.html             # Jinja2 templates (optional)
```

---

## 🔄 Arsitektur High-Level

```
Dashboardku (Docker)
├── Frontend (UI untuk manage task & project)
├── Backend API (CRUD task, project, webhook config)
├── Scheduler Service (Cek deadline & trigger notifikasi)
└── Database (MySQL)
```

---

## 🔄 Alur Notifikasi

```
┌─────────────────────────────────────────────────────────┐
│  1. User buat task dengan deadline                        │
│     → Scheduler simpan job                                │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  2. APScheduler run setiap 1 menit                       │
│     → Cek task yang deadline dalam X jam/hari            │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  3. Jika match, trigger notifikasi                       │
│     → Render template pesan                             │
│     → POST ke WAHA webhook                               │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  4. Log notifikasi ke database                           │
│     → Retry jika gagal (exponential backoff)            │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Data Model

### Projects
```sql
CREATE TABLE projects (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    color VARCHAR(7) DEFAULT '#3B82F6',
    icon VARCHAR(50),
    archived BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tasks
```sql
CREATE TABLE tasks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    priority ENUM('low', 'medium', 'high') DEFAULT 'medium',
    status ENUM('todo', 'in_progress', 'done') DEFAULT 'todo',
    deadline DATETIME,
    completed_at DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);
```

### Reminders
```sql
CREATE TABLE reminders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    task_id INT,
    reminder_type ENUM('day_h', 'relative', 'absolute'),
    relative_value INT,           -- NULL untuk day_h/absolute
    relative_unit ENUM('minutes', 'hours', 'days'), -- NULL untuk day_h/absolute
    absolute_time DATETIME,        -- NULL untuk day_h/relative
    sent BOOLEAN DEFAULT FALSE,
    sent_at DATETIME,
    FOREIGN KEY (task_id) REFERENCES tasks(id)
);
```

### Webhook Config
```sql
CREATE TABLE webhook_configs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    endpoint_url VARCHAR(2048) NOT NULL,
    headers JSON,                  -- Custom headers (Authorization, dll)
    message_template TEXT,         -- Template pesan WA
    is_active BOOLEAN DEFAULT TRUE
);
```

### Notification Logs
```sql
CREATE TABLE notification_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    task_id INT,
    reminder_id INT,
    webhook_config_id INT,
    status ENUM('pending', 'sent', 'failed'),
    response_code INT,
    response_body TEXT,
    retry_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🎨 Core Features Detail

### 1. Project Management
- Create/Read/Update/Delete Project
- Color coding per project (hex color picker)
- Icon/emoji untuk visual identification
- Archive project (soft delete)

### 2. Task Management
- CRUD Task dalam project
- **Fields:**
  - `title`: Task name (required)
  - `description`: Detailed notes (optional)
  - `priority`: low/medium/high
  - `status`: todo/in_progress/done
  - `deadline`: Datetime (nullable)
- Sub-task (optional, untuk task kompleks)
- Tag/label untuk kategorisasi lebih lanjut

### 3. Flexible Reminder System

#### Jenis Reminder
**a) Day H Reminder** (Default)
- Notifikasi tepat di hari H deadline
- Otomatis dibuat untuk setiap task dengan deadline

**b) Relative Reminder** (Custom)
- Notifikasi X satuan waktu sebelum deadline
- Contoh:
  - 2 hari sebelum deadline
  - 2 jam sebelum deadline
  - 30 menit sebelum deadline
- Bisa multiple reminder per task

**c) Absolute Reminder** (Advanced)
- Notifikasi di tanggal & jam spesifik
- Contoh: Reminder tiap hari senin jam 9 pagi
- Untuk recurring check-in

### 4. Webhook Integration
- Single/multiple endpoint webhook (POST)
- **Template pesan dengan variables:**
  ```text
  🔔 Reminder: {task_title}
  📁 Project: {project_name}
  ⏰ Deadline: {deadline}
  📝 Catatan: Tetap semangat!
  ```
- **Retry mechanism:**
  - 3x retry dengan exponential backoff
  - Retry delay: 30s, 60s, 120s
- **Custom headers** untuk authentication ke WAHA

### 5. Simple Authentication
- Single username/password
- Basic Auth atau API Key di header
- Session management sederhana

---

## 🌐 API Endpoints

### Authentication
```
POST   /api/login                          # Login (basic auth)
```

### Projects
```
GET    /api/projects                       # List all projects
POST   /api/projects                       # Create project
PUT    /api/projects/{id}                  # Update project
DELETE /api/projects/{id}                  # Delete project
PATCH  /api/projects/{id}/archive          # Archive project
```

### Tasks
```
GET    /api/projects/{id}/tasks            # List tasks in project
POST   /api/projects/{id}/tasks            # Create task
PUT    /api/tasks/{id}                     # Update task
DELETE /api/tasks/{id}                     # Delete task
PATCH  /api/tasks/{id}/complete            # Mark task complete
GET    /api/tasks/{id}                     # Get single task
```

### Reminders
```
GET    /api/tasks/{id}/reminders           # Get reminders for task
POST   /api/tasks/{id}/reminders           # Add reminder
PUT    /api/reminders/{id}                 # Update reminder
DELETE /api/reminders/{id}                 # Delete reminder
```

### Webhook & Notifications
```
GET    /api/webhook/config                 # Get webhook config
PUT    /api/webhook/config                 # Update webhook config
GET    /api/notifications/logs             # Notification logs
POST   /api/notifications/test             # Test webhook
```

---

## 🐳 Docker Configuration

### docker-compose.yml
```yaml
services:
  dashboardku:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DB_HOST=mysql
      - DB_USER=dashboardku
      - DB_PASS=secret
      - WAHA_WEBHOOK_URL=https://your-waha-endpoint.com/webhook
    depends_on:
      - mysql
    volumes:
      - ./app:/app

  mysql:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=rootpass
      - MYSQL_DATABASE=dashboardku
      - MYSQL_USER=dashboardku
      - MYSQL_PASSWORD=secret
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"

volumes:
  mysql_data:
```

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### requirements.txt
```text
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pymysql==1.1.0
pydantic==2.5.0
pydantic-settings==2.1.0
apscheduler==3.10.4
python-multipart==0.0.6
jinja2==3.1.2
python-dotenv==1.0.0
```

---

## 🎯 Implementation Plan

### Phase 1: Foundation ✅ COMPLETE
- [x] Setup project structure
- [x] Docker & Docker Compose setup
- [x] Database models & migrations
- [x] Basic FastAPI structure

### Phase 2: Core CRUD ✅ COMPLETE
- [x] Authentication (bcrypt + HMAC token: Basic/Bearer/X-API-Key)
- [x] Project CRUD API (+ archive soft-delete)
- [x] Task CRUD API + Auto Day-H Reminder sync
- [x] Reminder CRUD API (+ validasi per tipe)
- [x] Stats endpoint (bonus untuk dashboard)

### Phase 3: Notification System ✅ COMPLETE
- [x] Scheduler implementation (APScheduler, tiap 1 menit)
- [x] Reminder checker logic (Day-H, Relative, Absolute)
- [x] Webhook service (POST ke WAHA + custom headers)
- [x] Retry mechanism (exponential backoff)
- [x] Notification logging ke database
- [x] Webhook config & test endpoints

### Phase 4: Frontend ✅ COMPLETE
- [x] Login page (localStorage token persistence)
- [x] Project management UI (grid + color-coded cards)
- [x] Task management UI (filter, priority badge, deadline indicator)
- [x] Reminder configuration UI (backend API ready)
- [x] Notification log viewer
- [x] Stats dashboard + toast notifications + responsive mobile

### Phase 5: Testing & Deployment ✅ COMPLETE
- [x] End-to-end testing (14/14 checks passed — auth, CRUD, reminder, scheduler, frontend)
- [x] Docker compose build & run (MySQL healthy check)
- [x] Git repository initialized (initial commit + security fix)
- [x] Documentation final (README, TRACKER, TESTING_DEPLOYMENT, phase summaries)

---

## 📝 Notes & Considerations

### Security
- Password disimpan sebagai hash (bcrypt)
- API key rotation (opsional untuk production)
- HTTPS untuk production deployment

### Performance
- Database indexing pada `deadline` dan `task_id`
- Async/await untuk semua I/O operations
- Scheduler tidak blocking API server

### Extensibility
- Mudah menambah endpoint webhook baru
- Template pesan bisa di-runtime edit
- Support untuk multiple notification channel (future)

---

## 🔗 References
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [APScheduler Documentation](https://apscheduler.readthedocs.io/)
- [WAHA (WhatsApp Gateway)](https://waha.devlike.pro/)
- [Uptime Kuma Webhook Format](https://github.com/louislam/uptime-kuma)

---

**Created:** 2026-08-18
**Version:** 1.0 - MVP Specification
**Status:** ✅ ALL 5 PHASES COMPLETE
