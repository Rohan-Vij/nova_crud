"""Testing file for retrieving all the data from the API."""
import time
import pytest

@pytest.mark.order(1)
def test_alldata(api_data):
    """
    Test the /datas endpoint.
    """
    res, data = api_data

    assert res.status_code == 200, "Response should be 200."
    assert isinstance(data, list) is True, "Response should be a list."
    assert len(data) > 2, "Response list should have more than 2 items."
    assert isinstance(data[0], dict) is True, "Response should be a list of dictionaries."

