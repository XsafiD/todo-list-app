"""Decorator proteksi endpoint (16-security.md)."""
from functools import wraps

from flask import flash, redirect, session, url_for


def login_required(f):
    """Redirect ke login bila belum ada session user (UX), selalu @wraps(f)."""
    @wraps(f)
    def _wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Anda harus login terlebih dahulu.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return _wrapper
