import pytest
from subprocess import Popen

import pymongo
import uvicorn

from api.ddbapi.app.app import app
from test_data import acquisition_data

mongoclient = pymongo.MongoClient('mongodb://localhost:27017')
db = mongoclient['testdb']

class TestServer:
    def __init__(self):
        self.run_args = [
            'gunicorn',
            'ddbapi.app.app:app',
            '-b', '0.0.0.0:5001',
            '-k', 'uvicorn.workers.UvicornWorker',
        ]
        self.proc = None

    def init_proc(self):
        self.proc = Popen(self.run_args)

    def stop_proc(self):
        self.proc.terminate()

@pytest.fixture(scope="session", autouse=True)
def server(request):
    test_server = TestServer()
    print('Starting server')
    test_server.init_proc()

    def teardown():
        print('Tearing down server')
        test_server.stop_proc()
    
    request.addfinalizer(teardown)

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