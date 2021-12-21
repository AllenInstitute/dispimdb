import copy
import os
import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.ddbapi.app.app import app
from tests.conftest import good_acquisitions

client = TestClient(app)

def test_create_acquisition(mongo_delete_acq_after, good_acquisitions):
    for acquisition in good_acquisitions:
        acquisition_url = os.path.join('api/', 'new_acquisition')

        post_acq = copy.deepcopy(acquisition)
        post_acq.pop('acquisition_id')
        response = client.post(acquisition_url, json=post_acq)
        acquisition_data = response.json()

        assert response.status_code == 201
        assert acquisition_data['specimen_id'] == acquisition['specimen_id']
        assert acquisition_data['acquisition_id'] == acquisition['acquisition_id']

def test_get_acquisitions(mongo_insert_delete_acq, good_acquisitions, specimen_id):
    acq_list = []
    for acquisition in good_acquisitions:
        acq_list.append(acquisition['acquisition_id'])
    
    acquisition_url = os.path.join('api/',
        specimen_id,
        'acquisitions')
    
    response = client.get(acquisition_url)
    acquisition_data = response.json()

    assert set(acquisition_data) == set(acq_list)

def test_get_acquisition(mongo_insert_delete_acq, good_acquisitions):
    for acquisition in good_acquisitions:
        acquisition_url = os.path.join('api/',
            'acquisition',
            acquisition['acquisition_id'])

        response = client.get(acquisition_url)
        acquisition_data = response.json()

        assert response.status_code == 200
        assert acquisition_data['specimen_id'] == acquisition['specimen_id']
        assert acquisition_data['acquisition_id'] == acquisition['acquisition_id']

def test_update_acquisition(mongo_insert_delete_acq, good_acquisitions):
    n5_directory = 'my_n5_dir'

    for acquisition in good_acquisitions:
        if '_id' in acquisition:
            acquisition.pop('_id')

        acquisition['data_location']['n5_dir'] = n5_directory

        acquisition_url = os.path.join('api/',
            'acquisition',
            acquisition['acquisition_id'])

        response = client.put(acquisition_url, json=acquisition)
        acquisition_data = response.json()

        assert response.status_code == 200
        assert acquisition_data['specimen_id'] == acquisition['specimen_id']
        assert acquisition_data['acquisition_id'] == acquisition['acquisition_id']
        assert acquisition_data['data_location']['n5_dir'] == n5_directory

def test_put_data_location(mongo_insert_delete_acq, good_acquisitions):
    n5_directory = {
        'name': 'my_n5_dir',
        'status': 'STARTED'
    }

    for acquisition in good_acquisitions:
        if '_id' in acquisition:
            acquisition.pop('_id')
        
        data_key = 'n5_directory'
        acquisition_url = os.path.join('api/',
            'acquisition',
            acquisition['acquisition_id'],
            'data_location',
            data_key)

        response = client.put(acquisition_url, json=n5_directory)
        acquisition_data = response.json()

        assert response.status_code == 200

def test_patch_data_location_status(mongo_insert_delete_acq, good_acquisitions):
    data_key = 'tiff_directory'
    new_state = 'IN_PROGRESS'

    for acquisition in good_acquisitions:
        if '_id' in acquisition:
            acquisition.pop('_id')
        
        print(acquisition)
        
        acquisition_url = os.path.join('api/',
            'acquisition',
            acquisition['acquisition_id'],
            'data_location',
            data_key,
            'status',
            new_state)
        
        response = client.patch(acquisition_url)
        print(response.json())
        acquisition_data = response.json()

        assert response.status_code == 200

def test_delete_acquisition(mongo_insert_delete_acq, good_acquisitions):
    for acquisition in good_acquisitions:
        acquisition_url = os.path.join('api/',
            'acquisition',
            acquisition['acquisition_id'])

        delete_response = client.delete(acquisition_url)
        get_response = client.get(acquisition_url)

        assert delete_response.status_code == 204
        assert get_response.status_code == 404