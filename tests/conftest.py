import pytest
import json
import random
from app import app as flask_app


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

_id = random.randint(10000, 99999) #out of function scope so this does not rerun

@pytest.fixture
def random_id():
    return _id