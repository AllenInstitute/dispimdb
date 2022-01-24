import os
import pymongo

DATABASE_URI = os.environ.get(
    "DISPIMDB_MONGO_URI",
    'mongodb://localhost:27017')
DATABASE_NAME = os.environ.get(
    "DISPIMDB_DATABASE_NAME",
    "testdb")


def _mongoclient_retry(func):
    def _mongoclient_retry_wrap(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except pymongo.errors.AutoReconnect:
            return func(self, *args, **kwargs)
    return _mongoclient_retry_wrap


class DispimDBMongo:
    def __init__(self, database_uri, database_name):
        self._mongoclient = pymongo.MongoClient(database_uri)
        self._database = self._mongoclient[DATABASE_NAME]

    @_mongoclient_retry
    def find_one(self, collection, *args, **kwargs):
        return self._database[collection].find_one(*args, **kwargs)

    @_mongoclient_retry
    def find(self, collection, *args, **kwargs):
        return self._database[collection].find(*args, **kwargs)

    @_mongoclient_retry
    def find_list(self, collection, *args, **kwargs):
        return [*self.find(collection, *args, **kwargs)]

    @_mongoclient_retry
    def update_one(self, collection, *args, **kwargs):
        return self._database[collection].update_one(*args, **kwargs)

    @_mongoclient_retry
    def delete_many(self, collection, *args, **kwargs):
        return self._database[collection].delete_many(*args, **kwargs)

    @_mongoclient_retry
    def insert_one(self, collection, *args, **kwargs):
        return self._database[collection].insert_one(*args, **kwargs)

    @_mongoclient_retry
    def find_one_and_update(self, collection, *args, **kwargs):
        return self._database[collection].find_one_and_update(*args, **kwargs)


dispimdb_mongo = DispimDBMongo(DATABASE_URI, DATABASE_NAME)

dispimdb = dispimdb_mongo._database
