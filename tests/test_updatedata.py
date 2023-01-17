import json
import pytest
import pytest

@pytest.mark.order(4)
def test_updatedata(app, client):

    document = {
        "Time": pytest.random_number+1,
        "Data": pytest.random_number/2,
        "Median": pytest.random_number*2,
        "Mean": pytest.random_number*6,
    }

    res = client.put(f"/data/{pytest.record_id}", json=document)
    data = json.loads(res.get_data(as_text=True))

    assert res.status_code == 200, "Response should be 200."
    assert isinstance(data, dict) is True, "Response should be a dictionary."

    res = client.get(f"/data/{pytest.record_id}")
    data = json.loads(res.get_data(as_text=True))

    assert res.status_code == 200, "Response should be 200."
    assert isinstance(data, dict) is True, "Response should be a dictionary."

    assert data['_id']['$oid'] == pytest.record_id, "Response should be the same as the request."
    assert data['Mean'] == pytest.random_number*6, "Mean of the data should be 6x the random number."