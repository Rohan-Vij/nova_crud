import json
import pytest

@pytest.mark.order(3)
def test_createdata(app, client):

    document = {
        "Data": pytest.random_number,
    }

    res = client.post("/datas", json=document)
    data = json.loads(res.get_data(as_text=True))

    assert res.status_code == 201, "Response should be 201."
    assert isinstance(data, dict) is True, "Response should be a dictionary."

    pytest.record_id = data['_id']['$oid']

    res = client.get(f"/data/{data['_id']['$oid']}")
    data = json.loads(res.get_data(as_text=True))

    assert res.status_code == 200, "Response should be 200."
    assert isinstance(data, dict) is True, "Response should be a dictionary."

    assert data['Data'] == document['Data'], "Response should be the same as the request."

    


