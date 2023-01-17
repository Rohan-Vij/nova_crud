import json

def test_alldata(api_data):
    res, data = api_data

    assert res.status_code == 200, "Response should be 200."
    assert isinstance(data, list) is True, "Response should be a list."
    assert len(data) > 5, "Response list should have more than 5 items."
    assert isinstance(data[0], dict) is True, "Response should be a list of dictionaries."


# python -m pytest