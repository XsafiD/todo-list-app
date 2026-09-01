"""
controllers/auth_controller.py — Blueprint ``auth_bp``.

Routes:
  - GET/POST /auth/setup  — setup awal: buat akun pertama (public, 404 setelah ada user)
  - GET/POST /auth/login  — login (public)
  - POST     /auth/logout — logout (login_required)
"""
from flask import Blueprint, abort, flash, redirect, render_template, session, url_for

from app.forms.auth_forms import LoginForm, SetupForm
from app.services.auth_service import auth_service
from app.utils.decorators import login_required

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/setup", methods=["GET", "POST"])
def setup():
    """Setup awal — buat akun pertama; tidak auto-login, redirect ke login.

    Setelah ada user, endpoint ini mati permanen (404) — tidak ada
    registrasi ulang.
    """
    if auth_service.has_any_user():
        abort(404)

    form = SetupForm()
    if form.validate_on_submit():
        try:
            auth_service.create_first_user(form.username.data, form.password.data)
        except ValueError:
            abort(404)  # race: user dibuat di antara guard dan create
        flash("Akun berhasil dibuat. Silakan masuk.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/setup.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = auth_service.verify_login(form.username.data, form.password.data)
        if user is None:
            flash("Username atau password salah.", "error")
        else:
            session["user_id"] = user.id
            session["username"] = user.username
            session.permanent = True
            return redirect(url_for("main.dashboard"))

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()
    flash("Anda telah keluar.", "success")
    return redirect(url_for("auth.login"))
