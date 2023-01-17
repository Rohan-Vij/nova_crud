"""Service to refresh the contents of the main MongoDB databse with information from the dataset."""

import os

import pymongo
import pandas as pd

from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

# connect to MongoDB Atlas cluster using connection string from .env file
client = pymongo.MongoClient(os.getenv("MONGO_URI"))

# use the main database and collection
db = client.main
data = db.data

# read data from dataset and remove the first column
df = pd.read_csv(os.getenv("CSV_FILE"))
df.pop(df.columns[0])

# drop the data collection to delete all previous data
data.drop()

# insert data into the collection
data.insert_many(df.to_dict("records"))
