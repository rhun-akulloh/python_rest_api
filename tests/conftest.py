import pytest

from app.routes import app


@pytest.fixture
def client():
    app.testing = True
    return app.test_client()
