import copy
import pytest

import uvicorn

import client.ddbclient
from client.ddbclient import acquisition

from api.ddbapi.app.app import app

@pytest.mark.skip
def test_post_acquisition(mongo_delete_acq_after, good_acquisitions):
    for acq in good_acquisitions:
        post_acq = copy.deepcopy(acq)
        post_acq.pop('acquisition_id')
        post_acq.pop('_id')
        acq_id = acquisition.post(post_acq)

        assert acq['acquisition_id'] == acq_id

@pytest.mark.skip
def test_get_acquisitions(mongo_insert_delete_acq, good_acquisitions, specimen_id):
    acq_list = []
    for acq in good_acquisitions:
        acq_list.append(acq['acquisition_id'])
    
    acqs = acquisition.get_all(specimen_id)

    assert set(acq_list) == set(acqs)

@pytest.mark.skip
def test_get_acquisition(mongo_insert_delete_acq, good_acquisitions):
    for acq in good_acquisitions:
        acq_get = acquisition.get(acq['acquisition_id'])

        assert acq_get['specimen_id'] == acq['specimen_id']
        assert acq_get['acquisition_id'] == acq['acquisition_id']

@pytest.mark.skip
def test_put_data_location(mongo_insert_delete_acq, good_acquisitions):
    data_key = 'n5_directory'
    n5_directory = {
        'name': 'my_n5_dir',
        'status': 'STARTED'
    }

    for acq in good_acquisitions:
        print(acq)
        if '_id' in acq:
            acq.pop('_id')
        
        response_json = acquisition.put_data_location(
            acq['acquisition_id'],
            data_key,
            n5_directory
        )

        assert data_key in response_json['data_location']

@pytest.mark.skip
def test_patch_data_location_status(mongo_insert_delete_acq, good_acquisitions):
    data_key = 'tiff_directory'
    new_state = 'IN_PROGRESS'

    for acq in good_acquisitions:
        if '_id' in acq:
            acq.pop('_id')
        
        response_json = acquisition.patch_status(
            acq['acquisition_id'],
            data_key,
            new_state
        )

        assert new_state == response_json['data_location'][data_key]['status']

@pytest.mark.skip
def test_delete_acquisition(mongo_insert_delete_acq, good_acquisitions):
    for acq in good_acquisitions:
        response_json = acquisition.delete(acq['acquisition_id'])

        assert response_json is None