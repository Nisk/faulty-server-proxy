import pytest
from Sanity import get_instance

@pytest.fixture
def app():
    app = get_instance()
    app.config["TESTING"] = True

    yield app

@pytest.fixture
def client(app):
    return app.test_client()