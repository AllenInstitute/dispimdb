import os
import pymongo

DATABASE_URI = os.environ.get(
    "DISPIMDB_MONGO_URI",
    'mongodb://localhost:27017')
client = pymongo.MongoClient(DATABASE_URI)
DATABASE_NAME = os.environ.get(
    "DISPIMDB_DATABASE_NAME",
    "testdb")
dispimdb = client[DATABASE_NAME]