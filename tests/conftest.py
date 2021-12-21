import pytest
from test_data import acquisition_data

import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['testdb']

@pytest.fixture(scope="function")
def mongo_delete_acq_after(request):
    acquisitions = db.acquisitions

    def teardown():
        acquisitions.drop()
    
    request.addfinalizer(teardown)

@pytest.fixture(scope="function")
def mongo_insert_delete_acq(request):
    acquisitions = db.acquisitions
    acquisitions.insert_many(acquisition_data.acq_good_doc)

    def teardown():
        acquisitions.drop()
    
    request.addfinalizer(teardown)

@pytest.fixture()
def good_acquisitions():
    return acquisition_data.acq_good_doc

@pytest.fixture()
def bad_acquisitions():
    return acquisition_data.acq_bad_doc

@pytest.fixture()
def specimen_id():
    return acquisition_data.acq_good_doc[0]['specimen_id']