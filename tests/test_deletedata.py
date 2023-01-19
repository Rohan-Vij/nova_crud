import json
import pytest

@pytest.mark.order(5)
def test_deletedata(app, client):

    # Deleting the data point while it exists
    res = client.delete(f"/data/{pytest.record_id}")
    data = json.loads(res.get_data(as_text=True))

    assert res.status_code == 200, "Response should be 200."
    assert isinstance(data, dict) is True, "Response should be a dictionary."
    assert data['message'] == 'Post deleted', "Response should include" \
        "information that the post was deleted."

    # Deleting the data point while it does not exist - the API should return an error
    res = client.delete(f"/data/{pytest.record_id}")
    data = json.loads(res.get_data(as_text=True))

    assert res.status_code == 404, "Response should be 404."

    # Checking to make sure the data point was deleted from the database
    res = client.get(f"/data/{pytest.record_id}")
    data = json.loads(res.get_data(as_text=True))

    assert res.status_code == 404, "Response should be 404."
