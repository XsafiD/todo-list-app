"""Core fixtures — fresh app + in-memory SQLite per test (15-testing.md #1)."""
import pytest

from app import create_app
from app.extensions import db
from app.models import User


class TestConfig:
    TESTING = True
    SECRET_KEY = "test-secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ENGINE_OPTIONS = {}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    APP_USERNAME = "admin"
    APP_PASSWORD = "test-password"


@pytest.fixture
def app():
    """App baru per test — create_all di awal, drop_all di akhir (isolation penuh)."""
    application = create_app(TestConfig)
    with application.app_context():
        db.create_all()
        user = User(username="tester")
        user.set_password("pass12345")
        db.session.add(user)
        db.session.commit()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def login_user(client):
    """Auth via session_transaction — bukan login HTTP berulang (15-testing #5)."""
    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["username"] = "tester"
