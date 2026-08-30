FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1
# FLASK_DEBUG/DEBUG TIDAK di image — via compose env_file (default false)

WORKDIR /app

# pymysql, cryptography, bcrypt tersedia sebagai wheel — TIDAK perlu gcc/libmysqlclient
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Non-root user (18-deployment.md #6)
RUN addgroup --system app && adduser --system --ingroup app app \
    && chmod +x entrypoint.sh \
    && chown -R app:app /app
USER app

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request;urllib.request.urlopen('http://localhost:5000/health', timeout=3)"

# Migrasi otomatis saat startup, lalu gunicorn (1 worker — scheduler jalan tepat 1x)
ENTRYPOINT ["./entrypoint.sh"]
