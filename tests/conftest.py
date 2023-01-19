"""
Entrypoint file for the API tests.
Contains variables used allthroughout the psuedo-E2E testing and the instance of the Flask API.
"""
import json
import pytest
from app import app as flask_app

def pytest_configure():
    """
    Set up global variables for the testing.
    """
    pytest.record_id = ""
    # pytest.random_number = random.randint(1, 1000000)
    pytest.random_number = 20


@pytest.fixture
def app():
    """An instance of the Flask app for testing."""
    yield flask_app


@pytest.fixture
# pylint: disable=redefined-outer-name
# necessary for pytest fixtures to work
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
# pylint: disable=redefined-outer-name
# necessary for pytest fixtures to work
def api_data(client):
    """A helper function to get all the data from the API."""
    res = client.get("/datas")
    data = json.loads(res.get_data(as_text=True))

    return res, data
