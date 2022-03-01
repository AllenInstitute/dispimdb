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
        mongo_delete_acq_generated_after):
    for acq in good_acquisitions:
        excluded_fields = {"acquisition_id", "_id"}
        post_acq = copy.deepcopy(
            {k: acq[k] for k in acq.keys() - excluded_fields})

        acq_id = apiclient.acquisition.post(post_acq)

        assert acq['acquisition_id'] == acq_id


def test_post_acquisition_get_created(
        apiclient, good_acquisitions,
        mongo_delete_acq_generated_after):
    ex_acq = good_acquisitions[0]
    excluded_fields = {"acquisition_id", "_id"}
    acq = copy.deepcopy(
        {k: ex_acq[k] for k in ex_acq.keys() - excluded_fields})
    specimen_id = acq["specimen_id"]
    session_id = acq["session_id"]
    section_num = acq["section_num"]
    # get empty section, specimen, session
    assert not apiclient.specimen.get_specimens()
    assert not apiclient.section.get_sections_from_specimen(
        specimen_id)
    assert not apiclient.session.get_sessions_from_specimen(
        specimen_id)

    acq_id = apiclient.acquisition.post(acq)

    assert (apiclient.specimen.get_specimen(specimen_id)["specimen_id"] ==
            specimen_id)
    assert (apiclient.session.get_session(
                specimen_id, session_id)["session_id"] ==
            session_id)
    assert (apiclient.section.get_section(
                specimen_id, section_num)["section_num"] ==
            section_num)


def test_post_acquisition_existing(
        apiclient, databased_good_acquisitions):
    acq = databased_good_acquisitions[0]
    excluded_fields = {"acquisition_id", "_id"}
    post_acq = copy.deepcopy(
        {k: acq[k] for k in acq.keys() - excluded_fields})

    with pytest.raises(Exception):
        _ = apiclient.acquisition.post(post_acq)


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
        'uri': 'my_n5_dir',
        'status': 'CREATING'
    }

    for acq in databased_good_acquisitions:
        response_json = apiclient.acquisition.put_data_location(
            acq['acquisition_id'],
            data_key,
            n5_directory
        )

        assert data_key in response_json['data_location']


def test_put_existing_data_location(
        apiclient, databased_good_acquisitions):
    acq = databased_good_acquisitions[-1]

    acq_id = acq['acquisition_id']
    location_key, location_dict = next(iter(
        acq["data_location"].items()))

    updated_dict = copy.deepcopy(dict(
        location_dict, **{
            "uri": location_dict["uri"] + "NOT"
            }))

    with pytest.raises(Exception):
        _ = apiclient.acquisition.put_data_location(
            acq_id,
            location_key,
            updated_dict
        )
    r = apiclient.acquisition.get(acq_id)
    assert r["data_location"][location_key] == location_dict


def test_patch_data_location_status(
        apiclient, databased_good_acquisitions):
    data_key = 'tiff_directory'
    new_state = 'COMPLETE'

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
    new_state = "DELETED"

    for acq in databased_good_acquisitions:
        with pytest.raises(Exception):
            _ = apiclient.acquisition.patch_status(
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
    new_state = "COMPLETE"

    acquisition_id = "not_an_acqid"

    with pytest.raises(Exception):
        _ = apiclient.acquisition.patch_status(
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
            _ = apiclient.acquisition.patch_status(
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


def test_query_acquisitions(
        apiclient, databased_good_acquisitions):
    acquisitions_copy = copy.deepcopy(databased_good_acquisitions)
    acq_ids = [acq["acquisition_id"] for acq in acquisitions_copy][:-1]

    query = {
        "filter": {"acquisition_id": {"$in": acq_ids}},
        "projection": {"_id": False}
    }
    results = apiclient.acquisition.query(query)

    result_acq_ids = [racq["acquisition_id"] for racq in results]
    assert result_acq_ids == acq_ids

    assert all([racq.get("_id") is None for racq in results])
