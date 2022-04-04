from datetime import datetime

from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import Response
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict
from starlette.status import HTTP_201_CREATED
import pymongo

from ddbapi.db.db import dispimdb_mongo
from ddbapi.db.states import data_location_state_table
from ddbapi.app.models.acquisition import (
    StartAcquisitionModel, DataLocationModel)
from ddbapi.app.models.base import MongoQueryModel
from ddbapi.app.utils import AppJSONResponse


router = APIRouter()


def generate_acquisition_id(acquisition):
    dt = datetime.fromisoformat(
        acquisition['acquisition_time_utc'])
    dt_string = dt.strftime('%Y%m%dT%H%M%S%fZ')
    return "_".join(map(str, (
        acquisition['specimen_id'],
        acquisition['section_num'],
        acquisition['session_id'],
        dt_string
    )))


@router.post('/new_acquisition',
             tags=['acquisitions'])
def create_acquisition(acquisition: StartAcquisitionModel = Body(...)):
    acquisition = jsonable_encoder(acquisition)

    specimen_dict = {'specimen_id': acquisition['specimen_id']}
    if not dispimdb_mongo.find_one(
            'specimens', specimen_dict):
        dispimdb_mongo.add_document(
            "specimens", specimen_dict)

    session_dict = {
        **specimen_dict,
        **{"session_id": acquisition["session_id"]}}
    if not dispimdb_mongo.find_one(
            "sessions", session_dict):
        dispimdb_mongo.add_document(
            "sessions",
            session_dict)

    section_dict = {
        **specimen_dict,
        **{"section_num": acquisition["section_num"]}
    }
    if not dispimdb_mongo.find_one(
            "sections", section_dict):
        dispimdb_mongo.add_document(
            "sections",
            section_dict)

    acquisition['acquisition_id'] = generate_acquisition_id(acquisition)

    try:
        new_acquisition = dispimdb_mongo.add_document(
            "acquisitions", acquisition)
    except pymongo.errors.DuplicateKeyError as e:
        raise HTTPException(
            status_code=409,
            detail=f"Cannot post acquisition: {e}"
        )

    created_acquisition = dispimdb_mongo.find_one(
        "acquisitions",
        {
            '_id': new_acquisition.inserted_id
        })
    created_acquisition.pop('_id')

    return AppJSONResponse(
        status_code=HTTP_201_CREATED,
        content=created_acquisition)


@router.get('/{specimen_id}/acquisitions',
            tags=['acquisitions'])
def get_acquisitions(specimen_id: str):
    acquisition_objects = dispimdb_mongo.find_list(
        "acquisitions",
        {
            'specimen_id': specimen_id
        }, projection={"_id": False, "acquisition_id": True})

    acquisitions = [acq["acquisition_id"] for acq in acquisition_objects]

    if acquisitions:
        return acquisitions

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'No acquisitions found for specimen {specimen_id}')


@router.get('/acquisition/{acquisition_id}',
            tags=['acquisitions'])
def get_acquisition(acquisition_id: str):
    acquisition = dispimdb_mongo.find_one(
        "acquisitions", {'acquisition_id': acquisition_id})

    if acquisition:
        acquisition.pop('_id')
        return acquisition

    raise HTTPException(
        status_code=404,
        detail=f'Acquisition {acquisition_id} not found')


@router.put("/acquisition/query", tags=["acquisitions"])
def query_acquisitions(query: MongoQueryModel = Body(...)):
    query_dict = jsonable_encoder(query)
    try:
        results = dispimdb_mongo.find_list("acquisitions", **query_dict)
        return AppJSONResponse(
            status_code=200,
            content=results)
    except pymongo.errors.ExecutionTimeout:  # pragma: no cover
        return HTTPException(
            status_code=500,
            detail=f"querying timed out. query dict: {query_dict}")


@router.patch(('/acquisition/{acquisition_id}/data_location/{data_key}'
               '/status/{state}'),
              tags=["acquisitions"])
def patch_data_location_status(acquisition_id: str,
                               data_key: str,
                               state: str):

    update_field = f"data_location.{data_key}.status"
    updated_acquisition = dispimdb_mongo.find_one_and_update(
        "acquisitions",
        {
            "acquisition_id": acquisition_id,
            update_field: {
                "$in": data_location_state_table.allowed_sources(state)
            }
        },
        {"$set": {update_field: state}},
        return_document=pymongo.ReturnDocument.AFTER
    )

    if updated_acquisition is None:
        if state not in data_location_state_table.states:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'State {state} does not exist')
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(f"{acquisition_id} {data_key} cannot "
                        f"transition to {state}")
            )

    updated_acquisition.pop('_id')
    return AppJSONResponse(
        status_code=status.HTTP_200_OK,
        content=updated_acquisition)


@router.put("/acquisition/{acquisition_id}/data_location/{data_key}",
            tags=["acquisitions"])
def put_data_location(acquisition_id: str,
                      data_key: str,
                      location: DataLocationModel = Body(...)):
    location_dict = jsonable_encoder(location)

    update_field = f"data_location.{data_key}"

    updated_acquisition = dispimdb_mongo.find_one_and_update(
        "acquisitions",
        {
            "acquisition_id": acquisition_id,
            update_field: {"$exists": False}
        },
        {"$set": {update_field: location_dict}},
        return_document=pymongo.ReturnDocument.AFTER
    )

    if updated_acquisition is None:
        acquisition = dispimdb_mongo.find_one(
            "acquisitions",
            {"acquisition_id": acquisition_id})
        if acquisition is None:
            raise HTTPException(
                status_code=404,
                detail=f"acquisition {acquisition_id} not found"
            )
        else:
            raise HTTPException(
                status_code=409,
                detail=f"acquisition {acquisition_id} has data key {data_key}"
            )
    _ = updated_acquisition.pop("_id")
    return AppJSONResponse(
        status_code=status.HTTP_200_OK,
        content=updated_acquisition
    )


@router.delete('/acquisition/{acquisition_id}',
               tags=['acquisitions'])
def delete_acquisition(acquisition_id: str):
    delete_result = dispimdb_mongo.delete_many(
        "acquisitions",
        {
            'acquisition_id': acquisition_id
        })

    if delete_result.deleted_count >= 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Acquisition {acquisition_id} not found')
