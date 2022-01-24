import os
from datetime import datetime

from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from typing import Any, Dict, Optional, List
from starlette.status import HTTP_201_CREATED
import pymongo

from ddbapi.db.db import dispimdb_mongo
from ddbapi.db.states import data_location_state_table
from ddbapi.app.models.acquisition import (
    StartAcquisitionModel,
    UpdateAcquisitionModel
)

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

def acquisition_with_id(acquisition):
    acq_id = generate_acquisition_id(acquisition)
    return dict(acquisition, **{'_id': acq_id})

router = APIRouter()

@router.post('/new_acquisition',
    tags=['acquisitions'])
def create_acquisition(acquisition: StartAcquisitionModel = Body(...)):
    acquisition = jsonable_encoder(acquisition)

    if not dispimdb_mongo.find_one(
            'specimens', {'specimen_id': acquisition['specimen_id']}):
        dispimdb_mongo.insert_one(
            "specimens",
            {
                'specimen_id': acquisition['specimen_id']
            })

    if not dispimdb_mongo.find_one(
            "specimens", {'session_id': acquisition['session_id']}):
        dispimdb_mongo.insert_one(
            "sessions",
            {
                'specimen_id': acquisition['specimen_id'],
                'session_id': acquisition['session_id']
            })

    acquisition['acquisition_id'] = generate_acquisition_id(acquisition)

    new_acquisition = dispimdb_mongo.insert_one(
        "acquisitions", acquisition)

    created_acquisition = dispimdb_mongo.find_one(
        "acquisitions",
        {
            '_id': new_acquisition.inserted_id
        })
    created_acquisition.pop('_id')

    return JSONResponse(status_code=HTTP_201_CREATED,
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

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'No acquisitions found for specimen {specimen_id}')

@router.get('/acquisition/{acquisition_id}',
    tags=['acquisitions'])
def get_acquisition(acquisition_id: str):
    acquisition = dispimdb_mongo.find_one(
        "acquisitions", {'acquisition_id': acquisition_id})

    if acquisition:
        acquisition.pop('_id')
        return acquisition

    raise HTTPException(status_code=404,
        detail=f'Acquisition {acquisition_id} not found')

@router.get('/acquisition/query',
    tags=['acquisitions'])
def query_acquisition(query: dict):
    acquisitions = []
    acq_cursor = dispimdb_mongo.find("acquisitions", dict)

    for acq in acq_cursor:
        acq.pop('_id')
        acquisitions.append(acq)

    return acquisitions

'''
@router.put('/acquisition/{acquisition_id}',
    tags=['acquisitions'])
def update_acquisition(acquisition_id: str,
                       acquisition: UpdateAcquisitionModel = Body(...)):
    acquisition = {k: v for k, v in acquisition.dict().items() if v is not None}

    if len(acquisition) >= 1:
        update_result = dispimdb['acquisitions'].update_one({
            'acquisition_id': acquisition_id
        }, {'$set': acquisition})

        updated_acquisition = dispimdb['acquisitions'].find_one({
            'acquisition_id': acquisition_id
        })

        if update_result.modified_count == 1 and updated_acquisition:
            updated_acquisition.pop('_id')
            return JSONResponse(status_code=status.HTTP_200_OK,
                content=updated_acquisition)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Acquisition {acquisition_id} not found')

@router.patch('/acquisition/{acquisition_id}',
    tags=['acquisitions'])
def patch_acquisition(acquisition_id: str,
                      data: dict):

    if len(data) >= 1:
        update_result = dispimdb['acquisitions'].update_one({
            'acquisition_id': acquisition_id
        }, {'$set': data})

        updated_acquisition = dispimdb['acquisitions'].find_one({
            'acquisition_id': acquisition_id
        })

        if update_result.modified_count == 1 and updated_acquisition:
            updated_acquisition.pop('_id')
            return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                content=updated_acquisition)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Acquisition {acquisition_id} not found')
'''


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
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=updated_acquisition)


@router.put("/acquisition/{acquisition_id}/data_location/{data_key}",
            tags=["acquisitions"])
def put_data_location(acquisition_id: str,
                      data_key: str,
                      request: Dict[Any, Any]):
    acquisition = dispimdb_mongo.find_one(
        "acquisitions",
        {
            "acquisition_id": acquisition_id
        })

    if data_key in acquisition["data_location"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Data location already exists')

    update_field = f"data_location.{data_key}"
    updated_doc = dispimdb_mongo.update_one(
         "acquisitions",
         {"acquisition_id": acquisition_id},
         {"$set": {update_field: request}},
    )

    updated_acquisition = dispimdb_mongo.find_one(
        "acquisitions",
        {
            "acquisition_id": acquisition_id
        })
    updated_acquisition.pop('_id')
    return JSONResponse(status_code=status.HTTP_200_OK,
        content=updated_acquisition)

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

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Acquisition {acquisition_id} not found')
