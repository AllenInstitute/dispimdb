import contextlib
import copy
import os
import posixpath

import pymongo
import pytest

from .dummy_ddbapi_server import run_dummy_server
from .test_data import acquisition_data

mongo_uri = os.getenv(
        "DISPIMDB_TEST_MONGODB_URI",
        "mongodb://localhost:27017")
mongo_db = os.getenv(
        "DISPIMDB_TEST_MONGODB_DB",
        "dispimdb_test_db")
ddbapi_test_url = os.getenv(
    "DISPIMDB_CLIENT_TEST_DISPIMDB_URL",
    "http://127.0.0.1:5001/")


@pytest.fixture(scope="session")
def mongoclient_mongodb():
    mongoclient = pymongo.MongoClient(mongo_uri)
    db = mongoclient[mongo_db]

    yield mongoclient, db


@pytest.fixture(scope="session")
def ddbapi_server_url(mongoclient_mongodb):
    # mongoclient, mongodb = mongoclient, mongodb
    with run_dummy_server(
            ddbapi_test_url, mongo_uri, mongo_db) as server_url:
        yield server_url


@pytest.fixture(scope="session")
def ddbapi_endpoint_url(ddbapi_server_url):
    yield posixpath.join(ddbapi_server_url, "api")


@pytest.fixture(scope="function")
def acquisitions(mongoclient_mongodb):
    mongoclient, mongodb = mongoclient_mongodb
    yield mongodb.acquisitions


@pytest.fixture(scope="function")
def good_acquisitions():
    return copy.deepcopy(acquisition_data.acq_good_doc)


@contextlib.contextmanager
def databased_collection(collection, items, drop_after=True):
    collection.insert_many(copy.deepcopy(items))
    yield
    if drop_after:
        collection.drop()


@pytest.fixture(scope="function")
def databased_good_acquisitions(acquisitions, good_acquisitions):
    with databased_collection(acquisitions, good_acquisitions):
        yield copy.deepcopy(good_acquisitions)


@pytest.fixture(scope="function")
def mongo_delete_acq_after(request, acquisitions):
    def teardown():
        acquisitions.drop()

    request.addfinalizer(teardown)


@pytest.fixture(scope="function")
def mongo_insert_delete_acq(request, acquisitions):
    acquisitions = acquisitions
    acquisitions.insert_many(acquisition_data.acq_good_doc)

    def teardown():
        acquisitions.drop()

    request.addfinalizer(teardown)


@pytest.fixture()
def bad_acquisitions():
    return acquisition_data.acq_bad_doc


@pytest.fixture()
def specimen_id():
    return acquisition_data.acq_good_doc[0]['specimen_id']
