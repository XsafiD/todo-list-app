"""Application factory Dashboardku — Flask."""
import os
from importlib import import_module

from flask import Blueprint, Flask, render_template

from app.config import Config


def create_app(config_class: type[Config] = Config) -> Flask:
    """Buat dan konfigurasi aplikasi Flask."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Di belakang proxy (cloudflared / tailscale serve, tepat 1 hop) agar
    # remote_addr & scheme benar (18-deployment.md #7)
    from werkzeug.middleware.proxy_fix import ProxyFix

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

    _init_extensions(app)
    _register_blueprints(app)
    _register_error_handlers(app)
    _register_template_filters(app)
    _register_cli(app)
    _init_scheduler(app)

    return app


def _init_extensions(app: Flask) -> None:
    from app.extensions import csrf, db

    db.init_app(app)
    csrf.init_app(app)


def _register_blueprints(app: Flask) -> None:
    """Register semua blueprint controllers terpusat.

    Loop + try/except ImportError agar foundation tidak crash saat modul
    belum ada (01-controller.md #6).
    """
    for module_name in ("main", "auth", "project", "task", "archive", "setting"):
        try:
            module = import_module(f"app.controllers.{module_name}_controller")
        except ImportError:
            continue
        for attr in vars(module).values():
            if isinstance(attr, Blueprint):
                app.register_blueprint(attr)


def _register_error_handlers(app: Flask) -> None:
    import logging
    import traceback
    from werkzeug.exceptions import HTTPException

    logger = logging.getLogger(__name__)

    @app.errorhandler(404)
    def handle_not_found(exc: HTTPException):
        logger.info(f"404 Not Found: {exc.description} | URL: {exc.request.url if hasattr(exc, 'request') else 'N/A'}")
        return render_template("error.html", error_code=404), 404

    @app.errorhandler(403)
    def handle_forbidden(exc: HTTPException):
        logger.warning(f"403 Forbidden: {exc.description} | URL: {exc.request.url if hasattr(exc, 'request') else 'N/A'}")
        return render_template("error.html", error_code=403), 403

    @app.errorhandler(500)
    def handle_internal_error(exc: Exception):
        logger.error(f"500 Internal Server Error: {str(exc)}", exc_info=True)

        error_details = str(exc) if app.config.get("DEBUG") else "Terjadi kesalahan internal server. Silakan coba lagi nanti."
        error_traceback = traceback.format_exc() if app.config.get("DEBUG") else None

        return render_template(
            "error.html",
            error_code=500,
            error_details=error_details,
            error_traceback=error_traceback,
        ), 500

    @app.errorhandler(Exception)
    def handle_unexpected_error(exc: Exception):
        logger.error(f"Unexpected error: {str(exc)}", exc_info=True)

        error_details = str(exc) if app.config.get("DEBUG") else "Terjadi kesalahan tak terduga. Tim teknis telah diberitahu."
        error_traceback = traceback.format_exc() if app.config.get("DEBUG") else None

        return render_template(
            "error.html",
            error_code=500,
            error_details=error_details,
            error_traceback=error_traceback,
        ), 500


def _register_template_filters(app: Flask) -> None:
    from app.utils.filters import register_filters

    register_filters(app)


def _register_cli(app: Flask) -> None:
    from app.cli import register_cli

    register_cli(app)


def _init_scheduler(app: Flask) -> None:
    """Start background scheduler — hanya di proses yang melayani request.

    Werkzeug debug reloader menjalankan parent + child; tanpa guard ini
    scheduler jalan dobel (job 23:59 tereksekusi dua kali).
    """
    if app.config.get("DEBUG") and os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        return
    from app.scheduler import init_scheduler

    init_scheduler(app)
