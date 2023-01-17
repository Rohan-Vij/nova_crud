import json
import random
import pytest

def test_createdata(app, client, random_id):
    record_id = random_id

    document = {
        "id": record_id,
        "Time": record_id+1,
        "Data": record_id/2,
        "Median": record_id*2,
        "Mean": record_id*3,
    }

    res = client.post("/datas", json=document)
    data = json.loads(res.get_data(as_text=True))

    assert res.status_code == 201, "Response should be 201."
    assert isinstance(data, dict) is True, "Response should be a dictionary."
    assert data['id'] == document['id'], "Response should be the same as the request."

    res = client.get(f"/data/{data['_id']['$oid']}")
    data = json.loads(res.get_data(as_text=True))

    assert res.status_code == 200, "Response should be 200."
    assert isinstance(data, dict) is True, "Response should be a dictionary."

    assert data['id'] == document['id'], "Response should be the same as the request."
    assert data['Time'] == document['Time'], "Response should be the same as the request."
    assert data['Data'] == document['Data'], "Response should be the same as the request."
    assert data['Median'] == document['Median'], "Response should be the same as the request."
    assert data['Mean'] == document['Mean'], "Response should be the same as the request."

