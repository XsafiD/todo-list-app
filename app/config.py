"""Konfigurasi aplikasi Flask — env-based, satu class untuk semua environment.

Env vars:
    SECRET_KEY, DEBUG, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS,
    APP_USERNAME, APP_PASSWORD (default seed user via `flask create-user`)
"""
import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


def _bool(value: str | None, default: str = "false") -> bool:
    return (value if value is not None else default).lower() in {"1", "true", "yes"}


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-fallback-JANGAN-dipakai-production")
    DEBUG = _bool(os.environ.get("DEBUG"))

    # Database — MySQL via Docker (docker compose up -d mysql)
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = int(os.environ.get("DB_PORT", "3306"))
    DB_NAME = os.environ.get("DB_NAME", "dashboardku")
    DB_USER = os.environ.get("DB_USER", "dashboardku")
    DB_PASS = os.environ.get("DB_PASS", "secret")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True, "pool_size": 10, "max_overflow": 20}

    # Session — minimum hardening (16-security.md)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    # HTTPS-only cookie — aktif via env di production (cloudflared/tailscale serve)
    SESSION_COOKIE_SECURE = _bool(os.environ.get("SESSION_COOKIE_SECURE"), default="false")
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)

    # Seed user default (dipakai `flask create-user` bila tanpa argumen).
    # APP_PASSWORD_HASH (bcrypt literal) diutamakan — password plain tidak
    # tersimpan di env production.
    APP_USERNAME = os.environ.get("APP_USERNAME", "admin")
    APP_PASSWORD = os.environ.get("APP_PASSWORD", "changeme")
    APP_PASSWORD_HASH = os.environ.get("APP_PASSWORD_HASH")

    # Background scheduler (arsip otomatis) — off di test, env-overridable
    SCHEDULER_ENABLED = _bool(os.environ.get("SCHEDULER_ENABLED"), default="true")
