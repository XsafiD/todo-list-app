#!/bin/bash
BASE="http://localhost:8000"
PASS=0; FAIL=0

check() {
  if [ "$1" = "$2" ]; then echo "✅ $3"; PASS=$((PASS+1))
  else echo "❌ $3 (expected $2, got $1)"; FAIL=$((FAIL+1)); fi
}

# 1. Health
CODE=$(curl -s -o /dev/null -w "%{http_code}" $BASE/health)
check "$CODE" "200" "Health check"

# 2. Login valid
TOKEN=$(curl -s -X POST $BASE/api/login -H "Content-Type: application/json" -d '{"username":"admin","password":"changeme"}' | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))" 2>/dev/null)
[ -n "$TOKEN" ] && { echo "✅ Login valid credentials"; PASS=$((PASS+1)); } || { echo "❌ Login valid credentials"; FAIL=$((FAIL+1)); }

# 3. Login invalid
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST $BASE/api/login -H "Content-Type: application/json" -d '{"username":"admin","password":"salah"}')
check "$CODE" "401" "Login invalid ditolak (401)"

# 4. Auth protection
CODE=$(curl -s -o /dev/null -w "%{http_code}" $BASE/api/projects)
check "$CODE" "401" "Endpoint terproteksi tanpa token (401)"

AUTH="Authorization: Bearer $TOKEN"

# 5. Create project
PROJ_ID=$(curl -s -X POST $BASE/api/projects -H "$AUTH" -H "Content-Type: application/json" -d '{"name":"E2E Final Test","color":"#10b981"}' | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null)
[ -n "$PROJ_ID" ] && { echo "✅ Create project (id=$PROJ_ID)"; PASS=$((PASS+1)); } || { echo "❌ Create project"; FAIL=$((FAIL+1)); }

# 6. List projects
CODE=$(curl -s -o /dev/null -w "%{http_code}" $BASE/api/projects -H "$AUTH")
check "$CODE" "200" "List projects"

# 7. Create task with deadline today (triggers Day-H)
DEADLINE=$(date -u +"%Y-%m-%dT23:59:00")
TASK_ID=$(curl -s -X POST $BASE/api/projects/$PROJ_ID/tasks -H "$AUTH" -H "Content-Type: application/json" -d "{\"title\":\"E2E Final Task\",\"priority\":\"high\",\"deadline\":\"$DEADLINE\"}" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null)
[ -n "$TASK_ID" ] && { echo "✅ Create task (id=$TASK_ID)"; PASS=$((PASS+1)); } || { echo "❌ Create task"; FAIL=$((FAIL+1)); }

# 8. Auto Day-H reminder
DAYH=$(curl -s $BASE/api/tasks/$TASK_ID/reminders -H "$AUTH" | python3 -c "import sys,json; print(sum(1 for r in json.load(sys.stdin) if r['reminder_type']=='day_h'))" 2>/dev/null)
check "$DAYH" "1" "Auto Day-H reminder terbuat"

# 9. Complete toggle
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X PATCH $BASE/api/tasks/$TASK_ID/complete -H "$AUTH")
check "$CODE" "200" "Toggle complete task"

# 10. Stats
STATS=$(curl -s $BASE/api/stats -H "$AUTH" | python3 -c "import sys,json; d=json.load(sys.stdin); print('ok' if d['total_tasks']>0 else 'empty')" 2>/dev/null)
check "$STATS" "ok" "Stats endpoint"

# 11. Scheduler status
SCHED=$(curl -s $BASE/scheduler/status | python3 -c "import sys,json; print(json.load(sys.stdin)['running'])" 2>/dev/null)
check "$SCHED" "True" "Scheduler running"

# 12. Notification logs
CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/api/notifications/logs?limit=5" -H "$AUTH")
check "$CODE" "200" "Notification logs"

# 13. Frontend loads
FRONT=$(curl -s $BASE/ | grep -c "Dashboardku")
[ "$FRONT" -gt 0 ] && { echo "✅ Frontend index.html tersaji"; PASS=$((PASS+1)); } || { echo "❌ Frontend"; FAIL=$((FAIL+1)); }

# 14. Swagger docs
CODE=$(curl -s -o /dev/null -w "%{http_code}" $BASE/docs)
check "$CODE" "200" "Swagger UI (/docs)"

# Cleanup
curl -s -X DELETE $BASE/api/tasks/$TASK_ID -H "$AUTH" > /dev/null
curl -s -X DELETE $BASE/api/projects/$PROJ_ID -H "$AUTH" > /dev/null

echo -e "\n═══════════════════════════════"
echo "RESULT: $PASS passed, $FAIL failed"
echo "═══════════════════════════════"
