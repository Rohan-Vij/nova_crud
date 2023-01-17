import pytest
import json
import random
from app import app as flask_app

def pytest_configure():
    pytest.record_id = ""
    pytest.random_number = random.randint(1, 1000000)

@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def api_data(app, client):
    res = client.get("/datas")
    data = json.loads(res.get_data(as_text=True))

    return res, data
