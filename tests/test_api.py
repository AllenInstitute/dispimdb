import copy
import os
import posixpath

from fastapi.testclient import TestClient

from api.ddbapi.app.app import app

client = TestClient(app)


def test_create_acquisition(mongo_delete_acq_generated_after,
                            good_acquisitions):
    acquisition_url = os.path.join('api/', 'new_acquisition')
    for acquisition in good_acquisitions:

        post_acq = copy.deepcopy(acquisition)
        post_acq.pop('acquisition_id')
        response = client.post(acquisition_url, json=post_acq)
        acquisition_data = response.json()

        assert response.status_code == 201
        assert (acquisition_data['specimen_id'] ==
                acquisition['specimen_id'])
        assert (acquisition_data['acquisition_id'] ==
                acquisition['acquisition_id'])


def test_create_and_get_acquisition(mongo_delete_acq_generated_after,
                                    good_acquisitions):
    post_url = posixpath.join('api', 'new_acquisition')
    get_specimens_url = "api/specimens"

    expected_specimen_ids = {
        a["specimen_id"] for a in good_acquisitions}
    for acquisition in good_acquisitions:
        specimen_id = acquisition["specimen_id"]
        session_id = acquisition["session_id"]
        section_num = acquisition["section_num"]
        post_acq = copy.deepcopy(acquisition)
        post_acq.pop('acquisition_id')
        response = client.post(post_url, json=post_acq)
        acquisition_data = response.json()

        assert response.status_code == 201
        assert (acquisition_data['specimen_id'] ==
                acquisition['specimen_id'])
        assert (acquisition_data['acquisition_id'] ==
                acquisition['acquisition_id'])

        db_specimen_ids = [
            s["specimen_id"] for s in client.get(
                get_specimens_url).json()]
        assert specimen_id in db_specimen_ids
        assert len(db_specimen_ids) <= len(expected_specimen_ids)

        get_sessions_url = f"api/specimen/{specimen_id}/sessions"

        specimen_session_tups = [
            (s["specimen_id"], s["session_id"])
            for s in client.get(get_sessions_url).json()]
        assert (specimen_id, session_id) in specimen_session_tups

        get_sections_url = f"api/specimen/{specimen_id}/sections"
        specimen_section_tups = [
            (s["specimen_id"], s["section_num"])
            for s in client.get(get_sections_url).json()]
        assert (specimen_id, section_num) in specimen_section_tups


def test_create_acquisition_exists(databased_good_acquisitions):
    acquisition = databased_good_acquisitions[-1]

    acquisition_url = "api/new_acquisition"

    excluded_fields = {"acquisition_id", "_id"}
    post_acq = copy.deepcopy(
        {k: acquisition[k] for k in acquisition.keys() - excluded_fields})

    response = client.post(acquisition_url, json=post_acq)

    assert response.status_code == 409


def test_get_acquisitions(
        mongo_insert_delete_acq, good_acquisitions, specimen_id):
    acq_list = []
    for acquisition in good_acquisitions:
        acq_list.append(acquisition['acquisition_id'])

    acquisition_url = os.path.join(
        'api/',
        specimen_id,
        'acquisitions')

    response = client.get(acquisition_url)
    acquisition_data = response.json()

    assert set(acquisition_data) == set(acq_list)


def test_get_acquisition(mongo_insert_delete_acq, good_acquisitions):
    for acquisition in good_acquisitions:
        acquisition_url = os.path.join(
            'api/',
            'acquisition',
            acquisition['acquisition_id'])

        response = client.get(acquisition_url)
        acquisition_data = response.json()

        assert response.status_code == 200
        assert (acquisition_data['specimen_id'] ==
                acquisition['specimen_id'])
        assert (acquisition_data['acquisition_id'] ==
                acquisition['acquisition_id'])


def test_put_data_location(mongo_insert_delete_acq, good_acquisitions):
    n5_directory = {
        'uri': 'file:///path/to/my_n5_dir',
        'status': 'CREATING'
    }

    for acquisition in good_acquisitions:
        if '_id' in acquisition:
            acquisition.pop('_id')

        data_key = 'n5_directory'
        acquisition_url = os.path.join(
            'api/',
            'acquisition',
            acquisition['acquisition_id'],
            'data_location',
            data_key)

        response = client.put(acquisition_url, json=n5_directory)
        _ = response.json()

        assert response.status_code == 200


def test_put_existing_data_location(databased_good_acquisitions):
    acq = databased_good_acquisitions[-1]

    acq_id = acq['acquisition_id']
    location_key, location_dict = next(iter(
        acq["data_location"].items()))

    updated_dict = copy.deepcopy(dict(
        location_dict, **{
            "uri": location_dict["uri"] + "NOT"
            }))

    url = f"api/acquisition/{acq_id}/data_location/{location_key}"

    response = client.put(url, json=updated_dict)

    assert response.status_code == 409


def test_patch_data_location_status(
        mongo_insert_delete_acq, good_acquisitions):
    data_key = 'tiff_directory'
    new_state = 'COMPLETE'

    for acquisition in good_acquisitions:
        if '_id' in acquisition:
            acquisition.pop('_id')

        acquisition_url = os.path.join(
            'api/',
            'acquisition',
            acquisition['acquisition_id'],
            'data_location',
            data_key,
            'status',
            new_state)

        response = client.patch(acquisition_url)
        _ = response.json()

        assert response.status_code == 200


def test_delete_acquisition(mongo_insert_delete_acq, good_acquisitions):
    for acquisition in good_acquisitions:
        acquisition_url = os.path.join(
            'api/',
            'acquisition',
            acquisition['acquisition_id'])

        delete_response = client.delete(acquisition_url)
        get_response = client.get(acquisition_url)

        assert delete_response.status_code == 204
        assert get_response.status_code == 404
