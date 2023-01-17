"""Entrypoint for the Flask app."""
# import necessary modules
import os
import json

from flask import Flask, jsonify, request

import pymongo
from bson import json_util, ObjectId

import pandas as pd

from dotenv import load_dotenv

# --------------------- CONFIG --------------------- #

# load environment variables from .env file
load_dotenv()

# create a new Flask app
app = Flask(__name__)

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

# --------------------- UTIL --------------------- #

def parse_json(json_data):
    """Parse JSON into a readable format."""
    return json.loads(json_util.dumps(json_data))

# --------------------- ROUTES --------------------- #

@app.route("/datas", methods=["GET"])
def get_data():
    """Get all data from the collection."""
    # find all data in the collection
    data_list = list(data.find())
    # return data as JSON
    return jsonify(parse_json(data_list)), 200

@app.route("/datas", methods=["POST"])
def create_data():
    """Create new data."""
    # get data from the request
    data_item = request.get_json()

    # insert data into the collection
    data.insert_one(data_item)

    return jsonify(parse_json(data_item)), 201

@app.route("/data/<_id>", methods=["GET"])
def find_by_id(_id):
    """Find data by id."""
    # find data by id in the collection
    data_item = data.find_one({"_id": ObjectId(_id)})

    if not data_item:
        return jsonify({"message": "Post not found"}), 404

    return jsonify(parse_json(data_item)), 200

@app.route("/data/<_id>", methods=["PUT"])
def update_by_id(_id):
    """Update data by id."""
    # get data from the request
    data_item = request.get_json()

    # update data by id in the collection
    data.update_one({"_id": ObjectId(_id)}, {"$set": data_item})

    return jsonify(parse_json(data_item)), 200

@app.route("/data/<_id>", methods=["DELETE"])
def delete_by_id(_id):
    """Delete data by id."""
    # delete data by id in the collection
    data.delete_one({"_id": ObjectId(_id)})

    return jsonify({"message": "Post deleted"}), 200

# --------------------- RUN --------------------- #

if RUN_APP:
    app.run(debug=True)
