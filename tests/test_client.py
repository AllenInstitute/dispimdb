import copy
import pytest

import client.ddbclient
from client.ddbclient import client


@pytest.fixture(scope="session")
def apiclient(ddbapi_endpoint_url):
    yield client.DispimDbClient(
        base_url=ddbapi_endpoint_url,
        subpath=""  # FIXME subpath currently required
    )


def test_post_acquisition(
        apiclient, good_acquisitions,
        mongo_delete_acq_after,
        # mongo_delete_sections_after,
        # mongo_delete_specimens_after,
        # mongo_delete_sessions_after
        ):

    for acq in good_acquisitions:
        excluded_fields = {"acquisition_id", "_id"}
        post_acq = copy.deepcopy(
            {k: acq[k] for k in acq.keys() - excluded_fields})

        acq_id = apiclient.acquisition.post(post_acq)

        assert acq['acquisition_id'] == acq_id


def test_get_acquisitions(
        apiclient, databased_good_acquisitions, specimen_id):
    acq_list = []
    for acq in databased_good_acquisitions:
        acq_list.append(acq['acquisition_id'])

    acqs = apiclient.acquisition.get_all(specimen_id)

    assert set(acq_list) == set(acqs)


def test_get_acquisition(
        apiclient, databased_good_acquisitions):
    for acq in databased_good_acquisitions:
        acq_get = apiclient.acquisition.get(acq['acquisition_id'])

        assert acq_get['specimen_id'] == acq['specimen_id']
        assert acq_get['acquisition_id'] == acq['acquisition_id']


def test_put_data_location(
        apiclient, databased_good_acquisitions):
    data_key = 'n5_directory'
    n5_directory = {
        'name': 'my_n5_dir',
        'status': 'STARTED'
    }

    for acq in databased_good_acquisitions:
        response_json = apiclient.acquisition.put_data_location(
            acq['acquisition_id'],
            data_key,
            n5_directory
        )

        assert data_key in response_json['data_location']


def test_patch_data_location_status(
        apiclient, databased_good_acquisitions):
    data_key = 'tiff_directory'
    new_state = 'IN_PROGRESS'

    for acq in databased_good_acquisitions:

        response_json = apiclient.acquisition.patch_status(
            acq['acquisition_id'],
            data_key,
            new_state
        )

        assert new_state == response_json['data_location'][data_key]['status']


def test_bad_transition_patch_data_location_status(
        apiclient, databased_good_acquisitions):
    data_key = "tiff_directory"
    new_state = "NOT_STARTED"

    for acq in databased_good_acquisitions:
        with pytest.raises(Exception):
            rj = apiclient.acquisition.patch_status(
                acq['acquisition_id'],
                data_key,
                new_state
            )

        db_acq = apiclient.acquisition.get(acq["acquisition_id"])
        assert (db_acq["data_location"][data_key]["status"] ==
                acq["data_location"][data_key]["status"])


def test_bad_acquisition_patch_data_location_status(
        apiclient, databased_good_acquisitions):
    data_key = "tiff_directory"
    new_state = "IN_PROGRESS"

    acquisition_id = "not_an_acqid"

    with pytest.raises(Exception):
        rj = apiclient.acquisition.patch_status(
            acquisition_id,
            data_key,
            new_state
        )


def test_bad_state_patch_data_location_status(
        apiclient, databased_good_acquisitions):
    data_key = "tiff_directory"
    new_state = "NOT_A_STATE"

    for acq in databased_good_acquisitions:
        with pytest.raises(Exception):
            rj = apiclient.acquisition.patch_status(
                acq['acquisition_id'],
                data_key,
                new_state
            )

        db_acq = apiclient.acquisition.get(acq["acquisition_id"])
        assert (db_acq["data_location"][data_key]["status"] ==
                acq["data_location"][data_key]["status"])


def test_delete_acquisition(
        apiclient, databased_good_acquisitions):
    for acq in databased_good_acquisitions:
        response_json = apiclient.acquisition.delete(acq['acquisition_id'])

        assert response_json is None
