"""CLI commands Dashboardku."""
import click
from flask import Flask, current_app

from app.extensions import db
from app.models import User


def register_cli(app: Flask) -> None:
    @app.cli.command("create-user")
    @click.option("--username", "-u", default=None, help="Username (default: APP_USERNAME env)")
    @click.option("--password", "-p", default=None, help="Password (default: APP_PASSWORD env)")
    def create_user(username: str | None, password: str | None) -> None:
        """Buat user awal; jika username sudah ada, perbarui password-nya."""
        username = username or current_app.config["APP_USERNAME"]
        password = password or current_app.config["APP_PASSWORD"]

        user = User.get_by_username(username)
        if user is None:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            action = "dibuat"
        else:
            user.set_password(password)
            action = "diperbarui (password di-reset)"
        db.session.commit()
        click.echo(f"User '{username}' {action}.")
