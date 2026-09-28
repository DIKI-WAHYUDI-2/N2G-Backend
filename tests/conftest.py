import pytest
import bcrypt
import sys
from unittest.mock import MagicMock

from apps.app import create_app, db
from apps.models.user import User


@pytest.fixture(scope="session")
def app():
    # Setup test environment
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
        "JWT_COOKIE_SECURE": False,
        "JWT_SECRET_KEY": "test-secret"
    })

    with app.app_context():
        # Create Tables
        db.create_all()

        # Hash password using bcrypt since user_repository checks with bcrypt
        hashed_pw = bcrypt.hashpw(
            'testpassword'.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        # Create dummy user for auth tests
        user = User(
            username='testadmin',
            password=hashed_pw,
            role='ADMIN'
        )

        db.session.add(user)
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def auth_tokens(client):
    """
    Helper fixture to log in and return tokens directly
    without modifying client state.
    """
    response = client.post(
        '/auth/login',
        json={
            "username": "testadmin",
            "password": "testpassword"
        }
    )

    return {
        "access_token": response.get_json()['role'],
        "cookies": response.headers.getlist('Set-Cookie')
    }