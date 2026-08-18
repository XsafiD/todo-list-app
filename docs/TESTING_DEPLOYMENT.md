# Dashboardku - Testing Guide & Deployment Manual

## 📋 Table of Contents
1. [Development Testing](#development-testing)
2. [End-to-End Testing](#end-to-end-testing)
3. [Production Deployment](#production-deployment)
4. [WAHA Integration Testing](#waha-integration-testing)
5. [Troubleshooting](#troubleshooting)

---

## Development Testing

### Quick Test Commands

```bash
cd /home/xsafi0/Documents/Working/Dashboardku

# Start MySQL only (for local development)
docker compose up -d mysql

# Wait for MySQL to be ready
sleep 10 && docker compose exec -T mysql mysqladmin ping -h localhost -uroot -prootpass

# Run migrations
alembic upgrade head

# Start uvicorn server in background
nohup .venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > uvicorn.log 2>&1 &

# Wait for server
sleep 3
```

### API Testing Scripts

#### Test Authentication
```bash
#!/bin/bash
# test_auth.sh

echo "Testing Authentication..."

# Test login
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"changeme"}' | python3 -m json.tool

# Test invalid credentials
echo -e "\n\nTesting Invalid Credentials:"
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"wrong"}' | python3 -m json.tool

# Get token for subsequent tests
TOKEN=$(curl -s -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"changeme"}' | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

echo -e "\n\nToken obtained: ${TOKEN:0:50}..."
echo "$TOKEN" > /tmp/test_token.txt
```

#### Test Projects API
```bash
#!/bin/bash
# test_projects.sh

TOKEN=$(cat /tmp/test_token.txt)

echo "Testing Projects API..."

# List projects
echo "1. List Projects:"
curl -s http://localhost:8000/api/projects -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Create project
echo -e "\n2. Create Project:"
curl -s -X POST http://localhost:8000/api/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Project","color":"#ff6b6b"}' | python3 -m json.tool

# Get project ID from previous response
PROJECT_ID=$(curl -s http://localhost:8000/api/projects -H "Authorization: Bearer $TOKEN" | python3 -c "import sys, json; print(json.load(sys.stdin)[0]['id'])")

# Update project
echo -e "\n3. Update Project:"
curl -s -X PUT http://localhost:8000/api/projects/$PROJECT_ID \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Updated Project Name","color":"#3b82f6"}' | python3 -m json.tool

# Archive project
echo -e "\n4. Archive Project:"
curl -s -X PATCH http://localhost:8000/api/projects/$PROJECT_ID/archive?archived=true \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Delete project
echo -e "\n5. Delete Project:"
curl -s -X DELETE http://localhost:8000/api/projects/$PROJECT_ID \
  -H "Authorization: Bearer $TOKEN" -w "\nHTTP Status: %{http_code}\n"
```

#### Test Tasks API
```bash
#!/bin/bash
# test_tasks.sh

TOKEN=$(cat /tmp/test_token.txt)

echo "Testing Tasks API..."

# Create task with deadline
echo "1. Create Task with Deadline:"
DEADLINE=$(date -u -d "+3 days" +"%Y-%m-%dT%H:%M:%S")
curl -s -X POST http://localhost:8000/api/projects/1/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Task Test\",\"priority\":\"high\",\"deadline\":\"$DEADLINE\"}" | python3 -m json.tool

# List tasks
echo -e "\n2. List All Tasks:"
curl -s http://localhost:8000/api/tasks -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Filter by status
echo -e "\n3. Filter Tasks by Status (todo):"
curl -s "http://localhost:8000/api/tasks?status_filter=todo" -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

#### Test Notifications System
```bash
#!/bin/bash
# test_notifications.sh

TOKEN=$(cat /tmp/test_token.txt)

echo "Testing Notification System..."

# Check scheduler status
echo "1. Scheduler Status:"
curl -s http://localhost:8000/scheduler/status | python3 -m json.tool

# Configure webhook
echo -e "\n2. Configure Webhook:"
curl -s -X POST http://localhost:8000/api/webhook/config \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"WAHA Test","endpoint_url":"https://httpbin.org/post","message_template":"🔔 Reminder: {task_title}"}' | python3 -m json.tool

# List notification logs
echo -e "\n3. Notification Logs:"
curl -s "http://localhost:8000/api/notifications/logs?limit=10" -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Send test notification
echo -e "\n4. Send Test Notification:"
curl -s "http://localhost:8000/api/webhook/test?test_message=Hello+Dashboardku!" -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

### Python Test Suite

Run the comprehensive test suite:
```bash
python3 /tmp/test_api.py          # API functionality tests
python3 /tmp/test_notification_system.py  # Notification system tests
```

---

## End-to-End Testing

### Complete Flow Test

Create a bash script `test_full_flow.sh`:
```bash
#!/bin/bash

echo "=========================================="
echo "Full Flow Test: Create Task → Notification"
echo "=========================================="

TOKEN=$(cat /tmp/test_token.txt)

# Step 1: Create project
echo "✓ Creating project..."
curl -s -X POST http://localhost:8000/api/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"E2E Test Project","color":"#10b981"}'

# Get project ID
PROJECT_ID=$(curl -s http://localhost:8000/api/projects -H "Authorization: Bearer $TOKEN" | python3 -c "import sys,json; print([p['id'] for p in json.load(sys.stdin)][0])")
echo -e "\n✓ Created project ID: $PROJECT_ID"

# Step 2: Create task with TODAY deadline
echo "✓ Creating task with today's deadline..."
DEADLINE_TODAY=$(date -u +"%Y-%m-%dT23:59:00")
TASK_RESPONSE=$(curl -s -X POST http://localhost:8000/api/projects/$PROJECT_ID/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"URGENT E2E Test\",\"priority\":\"high\",\"deadline\":\"$DEADLINE_TODAY\"}")

echo "$TASK_RESPONSE" | python3 -m json.tool

TASK_ID=$(echo "$TASK_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo -e "\n✓ Created task ID: $TASK_ID"

# Step 3: Check auto Day-H reminder was created
echo "✓ Checking for auto Day-H reminder..."
REMINDERS=$(curl -s "http://localhost:8000/api/tasks/$TASK_ID/reminders" -H "Authorization: Bearer $TOKEN")
echo "$REMINDERS" | python3 -m json.tool

DAY_H_COUNT=$(echo "$REMINDERS" | python3 -c "import sys,json; reminders=json.load(sys.stdin); print(sum(1 for r in reminders if r['reminder_type']=='day_h'))")
echo -e "\n✓ Auto Day-H reminders created: $DAY_H_COUNT"

# Step 4: Wait for scheduler (runs every minute)
echo "⏳ Waiting 70 seconds for scheduler to trigger notification..."
sleep 70

# Step 5: Check notification logs
echo "✓ Checking notification logs..."
curl -s "http://localhost:8000/api/notifications/logs?task_id=$TASK_ID&limit=5" -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

echo -e "\n=========================================="
echo "✅ Full Flow Test Complete!"
echo "=========================================="
```

Execute the test:
```bash
chmod +x /tmp/test_full_flow.sh
/tmp/test_full_flow.sh
```

---

## Production Deployment

### Docker Deployment

#### Step 1: Prepare Environment
```bash
cd /home/xsafi0/Documents/Working/Dashboardku

# Generate strong SECRET_KEY
openssl rand -hex 32 > secret_key.txt

# Create hashed password (replace 'your_strong_password')
python3 -c "import bcrypt; print(bcrypt.hashpw('your_strong_password'.encode(), bcrypt.gensalt()).decode())" > APP_PASSWORD_HASH.txt
```

#### Step 2: Create Production .env
```bash
cat > .env.production << 'EOF'
DB_HOST=mysql
DB_PORT=3306
DB_NAME=dashboardku_prod
DB_USER=dashboardku_user
DB_PASS=<strong_random_password_here>

APP_USERNAME=admin
APP_PASSWORD_HASH=<the_hashed_password_above>
SECRET_KEY=$(cat secret_key.txt)

WAHA_WEBHOOK_URL=https://your-production-waha-instance.com/webhook

APP_ENV=production
DEBUG=false
EOF
```

#### Step 3: Build Docker Images
```bash
docker compose -f docker-compose.yml build --no-cache

# Or if you have a production docker-compose file
# docker compose -f docker-compose.prod.yml build
```

#### Step 4: Deploy
```bash
docker compose -f docker-compose.yml up -d

# Verify deployment
docker compose ps
docker compose logs -f dashboardku
```

#### Step 5: Run Migrations
```bash
docker compose exec dashboardku alembic upgrade head
```

#### Step 6: Verify Health
```bash
curl -s http://localhost:8000/health | python3 -m json.tool
curl -s http://localhost:8000/scheduler/status | python3 -m json.tool
```

### Local Production-Ready Deployment

For running without Docker in production:

#### Requirements
```bash
sudo apt-get update
sudo apt-get install -y python3.11 python3.11-venv default-libmysqlclient-dev nginx supervisor
```

#### Setup Process
```bash
cd /home/xsafi0/Documents/Working/Dashboardku

# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install production dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env.production
nano .env.production  # Edit with production values

# Run migrations
alembic upgrade head

# Start with gunicorn (production WSGI server)
gunicorn --bind 0.0.0.0:8000 --workers 4 --threads 2 app.main:app
```

#### Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static {
        alias /home/user/dashboardku/app/static;
    }
}
```

#### Supervisor Config
```ini
[program:dashboardku]
command=/home/user/dashboardku/.venv/bin/gunicorn --bind 0.0.0.0:8000 app.main:app
directory=/home/user/dashboardku
user=user
autostart=true
autorestart=true
stderr_logfile=/var/log/dashboardku/error.log
stdout_logfile=/var/log/dashboardku/out.log
```

---

## WAHA Integration Testing

### Test Webhook Delivery

Set up a simple webhook tester using httpbin or ngrok:

```bash
# Option 1: Using httpbin.org (public test endpoint)
curl -X POST https://httpbin.org/post \
  -H "Content-Type: application/json" \
  -d '{"message":"Test message","chatId":"+628123456789"}'

# Option 2: Using local ngrok tunnel
ngrok http 8000

# Then configure Dashboardku webhook URL to:
# https://abc123.ngrok.io/webhook/sendText/{phone}/{message}
```

### Expected Payload Format

When notification is sent, WAHA should receive:
```json
{
  "message": "🔔 Reminder: Review quarterly report\n📁 Project: Work\n⏰ Deadline: 2026-08-18",
  "context": {
    "task_id": 5,
    "project_id": 1,
    "reminder_id": 3,
    "test": false
  }
}
```

### WAHA Endpoint Examples

**Example 1: Direct sendText endpoint**
```
POST https://waha.yourcompany.com/webhook/sendText/+628123456789
Body: {"chatId":"+628123456789","text":"Reminder message..."}
```

**Example 2: Generic webhook**
```
POST https://waha.yourcompany.com/webhook
Body: {"message":"Reminder message...","target":"+628123456789"}
```

### Monitor WAHA Logs

Check if messages are being delivered:
```bash
docker logs waha-instance -f --tail 50
```

Look for successful delivery confirmations or error messages.

---

## Troubleshooting

### Common Issues

#### Issue 1: Database Connection Failed
```
Error: Can't connect to MySQL server
```

**Solution**:
```bash
# Check MySQL is running
docker compose ps mysql

# Restart MySQL
docker compose restart mysql

# Check connection
docker compose exec mysql mysql -u root -prootpass -e "SHOW DATABASES;"
```

#### Issue 2: Migration Errors
```
sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError) No such table
```

**Solution**:
```bash
# Reset database
docker compose down && docker volume rm dashboardku_mysql_data
docker compose up -d

# Re-run migrations
docker compose exec dashboardku alembic upgrade head
```

#### Issue 3: Scheduler Not Running
```
{"running":false} at /scheduler/status
```

**Solution**:
```bash
# Check server logs
docker logs dashboardku | grep -i scheduler

# Look for import errors
docker logs dashboardku --tail 100

# Restart container
docker compose restart dashboardku
```

#### Issue 4: Authentication Fails
```
401 Unauthorized on all requests
```

**Solution**:
```bash
# Verify password is correct
# Try logging in via curl
curl -X POST http://localhost:8000/api/login -H "Content-Type: application/json" -d '{"username":"admin","password":"changeme"}'

# If password hash issue, reset password in .env and regenerate hash
python3 -c "import bcrypt; print(bcrypt.hashpw('newpassword'.encode(), bcrypt.gensalt()).decode())"
```

#### Issue 5: Frontend Not Loading
```
404 when accessing root URL
```

**Solution**:
```bash
# Check static files exist
ls -la /home/xsafi0/Documents/Working/Dashboardku/app/static/index.html

# In Docker, verify mount points
docker compose ps

# Access directly
open http://localhost:8000/static/index.html
```

### Debug Mode

Enable detailed error reporting:
```bash
# Set DEBUG=true in .env
export DEBUG=true

# Or run locally with reload
uvicorn app.main:app --reload --log-level debug
```

### Log Analysis

Collect all relevant logs:
```bash
# Application logs
tail -f /path/to/uvicorn.log

# Database queries (with echo enabled)
docker compose exec dashboardku mysql -u dashboardku -psecret dashboardku -e "SHOW PROCESSLIST;"

# Network requests
tcpdump -i lo port 8000 -nn | grep HTTP
```

---

## Performance Benchmarks

### Response Time Targets

| Endpoint Type | Target | Acceptable |
|--------------|--------|------------|
| Health check | < 50ms | < 100ms |
| Auth login | < 200ms | < 500ms |
| CRUD operations | < 300ms | < 500ms |
| Stats query | < 150ms | < 300ms |
| Notification log | < 200ms | < 400ms |

### Load Testing

Basic load test using Apache Bench:
```bash
ab -n 100 -c 10 -p login.json -T "application/json" http://localhost:8000/api/login
ab -n 100 -c 10 http://localhost:8000/api/stats
```

Expected results:
- 100 requests in ~5-10 seconds
- Concurrent connections: 10
- Average response time: < 300ms

---

## Checklist Before Production

### Pre-Deployment Checklist

- [ ] Strong SECRET_KEY generated and set
- [ ] Password hashed with bcrypt
- [ ] DATABASE credentials secured
- [ ] WAHA_WEBHOOK_URL configured and tested
- [ ] HTTPS enabled (or plan for it)
- [ ] Database backups configured
- [ ] Monitoring tools installed (optional)
- [ ] Firewall rules configured
- [ ] Domain DNS pointed correctly
- [ ] Rate limiting considered

### Post-Deployment Verification

- [ ] Health endpoint responds (200 OK)
- [ ] Scheduler is running (`/scheduler/status` returns `"running":true`)
- [ ] Login works with new credentials
- [ ] Projects can be created and listed
- [ ] Tasks can be created with deadlines
- [ ] Notifications are logged
- [ ] Frontend loads correctly
- [ ] Mobile responsive design works
- [ ] Error pages display properly

---

**Document Version**: 1.0  
**Last Updated**: August 18, 2026  
**Maintained By**: Dashboardku Team
