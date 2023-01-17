import json
import random
import pytest

@pytest.mark.order(2)
def test_singledatapoint(app, client, api_data):
    res, data = api_data

    random_sample = random.sample(data, 5)

    for item in random_sample:
        # pylint: disable=unsubscriptable-object
        res = client.get(f"/data/{item['_id']['$oid']}")
        data = json.loads(res.get_data(as_text=True))

        assert res.status_code == 200, "Response should be 200."
        assert isinstance(data, dict) is True, "Response should be a dictionary."
        assert data['_id'] == item['_id'], "Response should be the same as the request."
