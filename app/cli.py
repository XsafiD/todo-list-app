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
        """Buat user awal; jika username sudah ada, perbarui password-nya.

        Prioritas password: opsi --password > APP_PASSWORD_HASH (bcrypt literal,
        untuk production) > APP_PASSWORD (plain, untuk dev).
        """
        username = username or current_app.config["APP_USERNAME"]

        user = User.get_by_username(username)
        if user is None:
            user = User(username=username)
            db.session.add(user)
            action = "dibuat"
        else:
            action = "diperbarui (password di-reset)"

        if password:
            user.set_password(password)
        elif current_app.config.get("APP_PASSWORD_HASH"):
            user.password_hash = current_app.config["APP_PASSWORD_HASH"]
        else:
            user.set_password(current_app.config["APP_PASSWORD"])

        db.session.commit()
        click.echo(f"User '{username}' {action}.")
