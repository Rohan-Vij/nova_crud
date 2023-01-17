import json
import random
import pytest

@pytest.mark.order(3)
def test_createdata(app, client):


    document = {
        "Time": pytest.random_number+1,
        "Data": pytest.random_number/2,
        "Median": pytest.random_number*2,
        "Mean": pytest.random_number*3,
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

    assert data['_id']['$oid'] == data['_id']['$oid'], "Response should be the same as the request."
    assert data['Time'] == document['Time'], "Response should be the same as the request."
    assert data['Data'] == document['Data'], "Response should be the same as the request."
    assert data['Median'] == document['Median'], "Response should be the same as the request."
    assert data['Mean'] == document['Mean'], "Response should be the same as the request."

