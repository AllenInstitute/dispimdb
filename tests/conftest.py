import pytest
from test_data.acquisition_data import acquisition_good_data

import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['testdb']

@pytest.fixture(scope="function")
def mongo_delete_acquisitions(request):
    acquisitions = db.acquisitions

    def teardown():
        acquisitions.drop()
    
    request.addfinalizer(teardown)

@pytest.fixture(scope="session")
def mongo_insert_acquisitions(request):
    acquisitions = db.acquisitions
    acquisitions.insert_many(acquisition_good_data)

    def teardown():
        acquisitions.drop()
    
    request.addfinalizer(teardown)

@pytest.fixture(scope="function")
def mongo_delete_sections(request):
    sections = db.sections

    def teardown():
        sections.drop()
    
    request.addfinalizer(teardown)

@pytest.fixture(scope="session")
def mongo_insert_sections(request):
    sections = db.sections
    sections.insert_many(section_good_data)

    def teardown():
        sections.drop()
    
    request.addfinalizer(teardown)

@pytest.fixture(scope="function")
def mongo_delete_sessions(request):
    sessions = db.sessions

    def teardown():
        sessions.drop()
    
    request.addfinalizer(teardown)

@pytest.fixture(scope="session")
def mongo_insert_sessions(request):
    sessions = db.sessions
    sessions.insert_many(session_good_data)

    def teardown():
        sessions.drop()
    
    request.addfinalizer(teardown)

@pytest.fixture()
def my_name():
    return "Sam Kinn".upper()

@pytest.fixture()
def list_of_numbers():
    return [1, 2, 3, 4]

@pytest.fixture()
def good_specimens():
    return specimen_good_data

@pytest.fixture()
def good_acquisitions():
    return acquisition_good_data

@pytest.fixture()
def good_sections():
    return section_good_data

@pytest.fixture()
def good_sessions():
    return session_good_data