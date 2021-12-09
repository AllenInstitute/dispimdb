import os
import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.ddbapi.app.app import app

client = TestClient(app)

def test_generate_acquisition_id():
    assert False

def test_create_acquisition(mongo_delete_acquisitions, good_acquisitions):
    for acquisition in good_acquisitions:
        acquisition_url = os.path.join('api/', 'new_acquisition')

        response = client.post(acquisition_url, json=acquisition)
        acquisition_data = response.json()

        assert response.status_code == 201
        assert acquisition_data['specimen_id'] == acquisition['specimen_id']
        assert acquisition['specimen_id'] in acquisition_data['acquisition_id']
        assert acquisition['session_id'] in acquisition_data['acquisition_id']

def test_get_acquisitions():
    assert False

def test_get_acquisition(mongo_insert_acquisitions, good_acquisitions):
    for acquisition in good_acquisitions:
        acquisition_url = os.path.join('api/',
            'acquisition',
            acquisition['acquisition_id'])

        response = client.get(acquisition_url)
        acquisition_data = response.json()

        assert response.status_code == 200
        assert acquisition_data['specimen_id'] == acquisition['specimen_id']
        assert acquisition_data['acquisition_id'] == acquisition['acquisition_id']

def test_query_acquisitions():
    assert False

def test_update_acquisition(mongo_insert_acquisitions, good_acquisitions):
    n5_directory = 'my_n5_dir'

    for acquisition in good_acquisitions:
        if '_id' in acquisition:
            acquisition.pop('_id')

        acquisition['data_location']['n5_directory'] = n5_directory

        acquisition_url = os.path.join('api/',
            'acquisition',
            acquisition['acquisition_id'])

        response = client.put(acquisition_url, json=acquisition)
        acquisition_data = response.json()

        assert response.status_code == 202
        assert acquisition_data['specimen_id'] == acquisition['specimen_id']
        assert acquisition_data['acquisition_id'] == acquisition['acquisition_id']
        assert acquisition_data['data_location']['n5_directory'] == n5_directory

def test_put_data_location():
    assert False

def test_patch_data_location_status():
    assert False

def test_delete_acquisition(mongo_insert_acquisitions, good_acquisitions):
    for acquisition in good_acquisitions:
        acquisition_url = os.path.join('api/',
            'acquisition',
            acquisition['acquisition_id'])

        delete_response = client.delete(acquisition_url)
        get_response = client.get(acquisition_url)

        assert delete_response.status_code == 204
        assert get_response.status_code == 404