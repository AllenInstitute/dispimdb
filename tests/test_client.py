import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from dispimdb_api.app.app import app

client = TestClient(app)

def test_create_specimen(mongo_delete_documents, good_specimens):
    for specimen in good_specimens:
        response = client.post('/', json=specimen)
        specimen_data = response.json()

        assert response.status_code == 201
        assert specimen_data['specimen_id'] == specimen['specimen_id']

def test_get_specimen(mongo_insert_documents, good_specimens):
    for specimen in good_specimens:
        response = client.get('/' + specimen['specimen_id'])
        specimen_data = response.json()

        assert response.status_code == 200
        assert specimen_data['specimen_id'] == specimen['specimen_id']
    
def test_update_specimen(mongo_insert_documents, good_specimens):
    updated_status = 'Finished'
    for specimen in good_specimens:
        if '_id' in specimen:
            specimen.pop('_id')
        
        specimen['status'] = updated_status
        response = client.put('/' + specimen['specimen_id'], json=specimen)
        specimen_data = response.json()
        
        assert response.status_code == 202
        assert specimen_data['specimen_id'] == specimen['specimen_id']
        assert specimen_data['status'] == specimen['status']
    
def test_delete_specimen(mongo_insert_documents, good_specimens):
    for specimen in good_specimens:
        delete_response = client.delete('/' + specimen['specimen_id'])
        get_response = client.get('/' + specimen['specimen_id'])

        assert delete_response.status_code == 204
        assert get_response.status_code == 404
    
def test_create_session():
    assert True

def test_get_session():
    assert True

def test_update_session():
    assert True

def test_delete_session():
    assert True

def test_create_acquisition():
    assert True

def test_get_acquisition():
    assert True

def test_update_acquisition():
    assert True

def test_delete_acquisition():
    assert True

def test_create_section():
    assert True

def test_get_section():
    assert True

def test_update_section():
    assert True

def test_delete_section():
    assert True