import pytest
from test_data.specimen_data import specimen_good_data
from test_data.acquisition_data import acquisition_good_data
from test_data.section_data import section_good_data
from test_data.session_data import session_good_data

import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['dispimdb']

@pytest.fixture(scope="function")
def mongo_delete_specimens(request):
    specimens = db.specimens

    def teardown():
        for specimen in specimen_good_data:
            specimens.delete_one({'specimen_id': specimen['specimen_id']})
    
    request.addfinalizer(teardown)

@pytest.fixture(scope="session")
def mongo_insert_specimens(request):
    specimens = db.specimens
    specimens.insert_many(specimen_good_data)

    def teardown():
        for specimen in specimen_good_data:
            specimens.delete_one({'specimen_id': specimen['specimen_id']})
    
    request.addfinalizer(teardown)

@pytest.fixture(scope="function")
def mongo_delete_acquisitions(request):
    acquisitions = db.acquisitions

    def teardown():
        for acquisition in acquisition_good_data:
            acquisitions.delete_one({
                'specimen_id': acquisition['specimen_id'],
                'acquisition_id': acquisition['acquisition_id']
            })
    
    request.addfinalizer(teardown)

@pytest.fixture(scope="session")
def mongo_insert_acquisitions(request):
    acquisitions = db.acquisitions
    acquisitions.insert_many(acquisition_good_data)

    def teardown():
        for acquisition in acquisition_good_data:
            acquisitions.delete_one({
                'specimen_id': acquisition['specimen_id'],
                'acquisition_id': acquisition['acquisition_id']
            })
    
    request.addfinalizer(teardown)

@pytest.fixture(scope="function")
def mongo_delete_sections(request):
    sections = db.sections

    def teardown():
        for section in section_good_data:
            sections.delete_one({
                'specimen_id': section['specimen_id'],
                'section_num': section['section_num']
            })
    
    request.addfinalizer(teardown)

@pytest.fixture(scope="session")
def mongo_insert_sections(request):
    sections = db.sections
    sections.insert_many(section_good_data)

    def teardown():
        for section in section_good_data:
            sections.delete_one({
                'specimen_id': section['specimen_id'],
                'section_num': section['section_num']
            })
    
    request.addfinalizer(teardown)

@pytest.fixture(scope="function")
def mongo_delete_sessions(request):
    sessions = db.sessions

    def teardown():
        for session in session_good_data:
            sessions.delete_one({
                'specimen_id': session['specimen_id'],
                'session_id': session['session_id']
            })
    
    request.addfinalizer(teardown)

@pytest.fixture(scope="session")
def mongo_insert_sessions(request):
    sessions = db.sessions
    sessions.insert_many(session_good_data)

    def teardown():
        for session in session_good_data:
            sessions.delete_one({
                'specimen_id': session['specimen_id'],
                'session_id': session['session_id']
            })
    
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