import json
import pytest

def test_updatedata(app, client, random_id):
    record_id = pytest.random_id

    document = {
        "id": record_id,
        "Time": record_id+1,
        "Data": record_id/2,
        "Median": record_id*2,
        "Mean": random_id*3,
    }

    res = client.post(f"/data/", json=document)
    data = json.loads(res.get_data(as_text=True))

    assert res.status_code == 201, "Response should be 201."
    assert isinstance(data, dict) is True, "Response should be a dictionary."