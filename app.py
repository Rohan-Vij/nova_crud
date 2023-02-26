"""Entrypoint for the Flask app."""

# pylint: disable=duplicate-code

# import necessary modules
import os
import json
import gzip
import time
import threading
import time

from flask import Flask, request
from flask_restx import Api, Resource, fields

import pymongo
from bson import json_util, ObjectId

import pandas as pd

from dotenv import load_dotenv

# --------------------- CONFIG --------------------- #

# load environment variables from .env file
load_dotenv()

# create a new Flask/Flask-RESTX app
app = Flask(__name__)
api = Api(app, validate=True)

# connect to MongoDB Atlas cluster using connection string from .env file
client = pymongo.MongoClient(os.getenv("MONGO_URI"))

if __name__ == "__main__":
    RUN_APP = True

    # use the main database and collection
    db = client.main
    data = db.data

else:
    RUN_APP = False

    # use the test database and collection
    db = client.test
    data = db.data

    # refresh the data collection for testing purposes (ensures consistency)

    # read data from dataset and remove the first column
    df = pd.read_csv(os.getenv("CSV_FILE"))
    df.pop(df.columns[0])

    # drop the data collection to delete all previous data
    data.drop()

    # insert data into the collection
    data.insert_many(df.to_dict("records"))

# calculate the sum and and number of documents in the database
running_list = [item['Data'] for item in data.find({}, {"_id": 0, "Data": 1})]

running_sum = sum(running_list)
running_count = len(running_list)

print(f"Running sum: {sum(running_list)}")
print(f"Running count: {len(running_list)}")

# --------------------- UTIL --------------------- #

def parse_json(json_data):
    """Parse JSON into a readable format."""
    return json.loads(json_util.dumps(json_data))

def find_median(lst):
    """Find the median of a list."""
    lst.sort()
    mid = len(lst) // 2
    res = (lst[mid] + lst[~mid]) / 2

    return res

# --------------------- DTOS --------------------- #


id_model = api.model('Id', {
    '$oid': fields.String(required=True)
})

data_model = api.model('Model', {
    '_id': fields.Nested(id_model, required=False),
    'Data': fields.Float(required=True),
    # the following fields are now calculated by the server
    # 'Mean': fields.Float(required=True),
    # 'Median': fields.Float(required=True),
    # 'Time': fields.Float(required=True)
})

# --------------------- DUMPING THREAD --------------------- #
# pylint: disable=fixme
# # TODO: is periodic checking more efficient than checking every
#         time a CRUD operation is performed?

def dump_collection():
    """Dumps the MongoD collection to a .gz (gzip) file if the collection grows too large in size"""
    while True:
        # get the size of the collection
        collection_data = list(data.find())
        collection_size = len(collection_data)

        # if the collection is too large, dump it to a .gz file
        if collection_size > 100:
            print("Collection size too large, dumping to .gz file...")

            # dump the data to a .gz file (unix timestamp in name)
            with gzip.open(f"dumps/{int(time.time())}_data.json.gz", "wt") as file:
                file.write(json.dumps(parse_json(collection_data)))

            # drop the collection
            data.drop()
        else:
            print(f"Only {collection_size} documents in the collection. No need to dump yet.")

        # wait for 60  seconds before checking again
        time.sleep(60)

dump_thread = threading.Thread(target=dump_collection)
dump_thread.start()

# --------------------- ROUTES --------------------- #


@api.route("/datas")
class ReadCreate(Resource):
    """Endpoint for reading and creating data."""
    # pylint: disable=global-statement

    def get(self):
        """Get all data from the collection."""
        # find all data in the collection
        data_list = list(data.find())
        # return data as JSON
        return parse_json(data_list), 200

    @api.expect(data_model)
    def post(self):
        """Create new a new data point."""
        # pylint: disable=global-statement, invalid-name
        # needs to be refactored sometime in the future - this is not good practice
        global running_sum, running_count

        # get data from the request
        data_item = request.get_json()

        # update the running sum and count
        # pylint: disable=redefined-outer-name
        running_count += 1
        running_sum += data_item['Data']
        running_list.append(data_item['Data'])

        # calculate the mean and median
        data_item['Time'] = running_count
        data_item['Median'] = find_median(running_list)
        data_item['Mean'] = running_sum / running_count

        # insert data into the collection
        data.insert_one(data_item)

        return parse_json(data_item), 201


@api.route("/data/<string:_id>")
class FindCreateDelete(Resource):
    """Find data by id."""

    def get(self, _id):
        """Get data by by its MongoDB-assigned id."""
        # find data by id in the collection
        data_item = data.find_one({"_id": ObjectId(_id)})

        if not data_item:
            return {"message": "Data point not found"}, 404

        return parse_json(data_item), 200

    @api.expect(data_model)
    def put(self, _id):
        """Update data by id."""
        # pylint: disable=global-statement, invalid-name
        # needs to be refactored sometime in the future - this is not good practice
        global running_sum, running_count

        # get data from the request
        data_item = request.get_json()

        # update data by id in the collection
        data.update_one({"_id": ObjectId(_id)}, {"$set": data_item})

        # find the data point
        data_item = data.find_one({"_id": ObjectId(_id)})

        if not data_item:
            return {"message": "Data point not found"}, 404

        running_list[data_item['Time'] - 1] = data_item['Data']

        # update the running sum and count
        # pylint: disable=redefined-outer-name
        running_sum = sum(running_list)
        running_count = len(running_list)

        all_data = list(data.find({}))

        for data_point in all_data:
            current_running_sum = sum(running_list[:data_point['Time']])
            current_running_count = data_point['Time']

            data_point['Mean'] = current_running_sum / current_running_count
            data_point['Median'] = find_median(running_list[:data_point['Time']])
            data_point['Time'] = data_point['Time']

            data.update_one({"_id": data_point['_id']}, {"$set": data_point})

        return parse_json(data_item), 200

    def delete(self, _id):
        """Delete data by id."""
        # pylint: disable=global-statement
        # needs to be refactored sometime in the future - this is not good practice

        # delete data by id in the collection
        delete = data.delete_one({"_id": ObjectId(_id)})

        # if nothing was deleted, return a 404
        if delete.deleted_count == 0:
            return {"message": "Post not found"}, 404

        for data_point in list(data.find({})):
            current_running_sum = sum(running_list[:data_point['Time']])
            current_running_count = data_point['Time']

            data_point['Mean'] = current_running_sum / current_running_count
            data_point['Median'] = find_median(running_list[:data_point['Time']])
            data_point['Time'] = data_point['Time']

            data.update_one({"_id": data_point['_id']}, {"$set": data_point})

        return {"message": "Post deleted"}, 200

# --------------------- RUN --------------------- #


if RUN_APP:
    app.run(debug=True)
