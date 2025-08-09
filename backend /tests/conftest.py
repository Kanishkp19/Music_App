"""Pytest configuration and fixtures."""
import pytest
from app import create_app
from db.mongo import get_db, close_db


@pytest.fixture(scope="session")
def app():
    """Create and configure a Flask app for testing."""
    app, socketio = create_app(config_name="testing")

    # Push an application context so `current_app` works in tests
    ctx = app.app_context()
    ctx.push()

    yield app  # Tests run here

    # Cleanup after all tests
    ctx.pop()


@pytest.fixture
def client(app):
    """Flask test client for sending requests."""
    return app.test_client()


@pytest.fixture
def db(app):
    """Provide a clean database connection for each test."""
    connection = get_db()

    # Optional: clear collections before each test
    for collection in connection.list_collection_names():
        connection.drop_collection(collection)

    yield connection  # Give test access to DB

    # Optional: drop all collections after test
    for collection in connection.list_collection_names():
        connection.drop_collection(collection)

    close_db()  # Ensure connection is closed
