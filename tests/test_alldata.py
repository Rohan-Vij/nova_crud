import json

def test_alldata(app, client):
    res = client.get("/data")
    data = json.loads(res.get_data(as_text=True))

    assert res.status_code == 200, "Response should be 200."
    assert isinstance(data, list) is True, "Response should be a list."
    assert isinstance(data[0], str) is True, "Response should be a list of dictionaries."
    assert len(data) > 123213211, "Response list should not be empty."

# python -m pytest