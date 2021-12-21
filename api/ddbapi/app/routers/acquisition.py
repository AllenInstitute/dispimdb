import os
from datetime import datetime

from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from typing import Any, Dict, Optional, List
from starlette.status import HTTP_201_CREATED

from ddbapi.db.db import dispimdb
from ddbapi.db.states import states, allowed_transitions
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

    if not dispimdb['specimens'].find_one({'specimen_id': acquisition['specimen_id']}):
        dispimdb['specimens'].insert_one({
            'specimen_id': acquisition['specimen_id']
        })

    if not dispimdb['specimens'].find_one({'session_id': acquisition['session_id']}):
        dispimdb['sessions'].insert_one({
            'specimen_id': acquisition['specimen_id'],
            'session_id': acquisition['session_id']
        })
    
    acquisition['acquisition_id'] = generate_acquisition_id(acquisition)

    new_acquisition = dispimdb['acquisitions'].insert_one(acquisition)

    created_acquisition = dispimdb['acquisitions'].find_one({
        '_id': new_acquisition.inserted_id
    })
    created_acquisition.pop('_id')

    return JSONResponse(status_code=HTTP_201_CREATED,
        content=created_acquisition)

@router.get('/{specimen_id}/acquisitions',
    tags=['acquisitions'])
def get_acquisitions(specimen_id: str):
    acquisitions = []
    acquisition_cursor = dispimdb['acquisitions'].find({
        'specimen_id': specimen_id
    })

    for acquisition in acquisition_cursor:
        acquisition.pop('_id')
        acquisitions.append(acquisition['acquisition_id'])
    
    if acquisitions:
        return acquisitions
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'No acquisitions found for specimen {specimen_id}')

@router.get('/acquisition/{acquisition_id}',
    tags=['acquisitions'])
def get_acquisition(acquisition_id: str):
    acquisition = dispimdb['acquisitions'].find_one({
        'acquisition_id': acquisition_id})

    if acquisition:
        acquisition.pop('_id')
        return acquisition
    
    raise HTTPException(status_code=404,
        detail=f'Acquisition {acquisition_id} not found')

@router.get('/acquisition/query',
    tags=['acquisitions'])
def query_acquisition(query: dict):
    acquisitions = []
    acq_cursor = dispimdb['acquisitions'].find(dict)

    for acq in acq_cursor:
        acq.pop('_id')
        acquisitions.append(acq)
    
    return acquisitions

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

'''
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

@router.patch('/acquisition/{acquisition_id}/data_location/{data_key}/status/{state}',
              tags=["acquisitions"])
def patch_data_location_status(acquisition_id: str,
                               data_key: str,
                               state: str):

    acquisition = dispimdb["acquisitions"].find_one({
        "acquisition_id": acquisition_id
    })

    if not state in states:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'State {state} does not exist')
    
    current_state = acquisition['data_location'][data_key]['status']
    if not state in allowed_transitions[current_state]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'State transition not allowed')

    update_field = f"data_location.{data_key}.status"
    updated_doc = dispimdb["acquisitions"].update_one(
        {"acquisition_id": acquisition_id},
        {"$set": {update_field: state}},
    )
    
    return JSONResponse(status_code=status.HTTP_200_OK)

@router.put("/acquisition/{acquisition_id}/data_location/{data_key}",
            tags=["acquisitions"])
def put_data_location(acquisition_id: str,
                      data_key: str,
                      request: Dict[Any, Any]):
    acquisition = dispimdb["acquisitions"].find_one({
        "acquisition_id": acquisition_id
    })

    if data_key in acquisition["data_location"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Data location already exists')

    update_field = f"data_location.{data_key}"
    updated_doc = dispimdb["acquisitions"].update_one(
         {"acquisition_id": acquisition_id},
         {"$set": {update_field: request}},
    )
    return JSONResponse(status_code=status.HTTP_200_OK)

@router.delete('/acquisition/{acquisition_id}',
    tags=['acquisitions'])
def delete_acquisition(acquisition_id: str):
    delete_result = dispimdb['acquisitions'].delete_many({
        'acquisition_id': acquisition_id
    })

    if delete_result.deleted_count >= 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Acquisition {acquisition_id} not found')