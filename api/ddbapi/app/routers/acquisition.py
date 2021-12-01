import os
from datetime import datetime

from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from typing import Optional, List
from starlette.status import HTTP_201_CREATED

from ddbapi.db.db import dispimdb
from ddbapi.app.models.acquisition import (
    StartAcquisitionModel,
    UpdateAcquisitionModel
)

def generate_acquisition_id(acquisition):
    dt = datetime.datetime.fromisoformat(
        acquisition["acquisition_time_utc"])
    dt_string = dt.strftime("%Y%m%dT%H:%M:%S:%fZ")
    return "_".join(map(str, (
        acquisition["specimen_id"],
        acquisition["session_id"],
        acquisition["section_num"],
        dt_string
    )))

def acquisition_with_id(acquisition):
    acq_id = generate_acquisition_id(acquisition)
    return dict(acquisition, **{"_id": acq_id})

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
    
    timestamp = datetime.now()
    timestamp_str = timestamp.strftime("%Y%m%d%H%M%S")
    acquisition_id = '_'.join([acquisition['specimen_id'],
        acquisition['session_id'],
        timestamp_str])
    
    acquisition['acquisition_id'] = acquisition_id

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
    
    raise HTTPException(status_code=404,
        detail=f'No acquisitions found for specimen {specimen_id}')

@router.get('/acquisition/{acquisition_id}',
    tags=['acquisitions'])
def get_acquisition(acquisition_id: str):
    #acquisition = dispimdb['acquisitions'].find_one({
    #    'specimen_id': specimen_id,
    #    'acquisition_id': acquisition_id})
    acquisition = []
    acq_cursor = dispimdb['acquisitions'].find({
        'acquisition_id': acquisition_id})
    for acq in acq_cursor:
        acq.pop('_id')
        acquisition.append(acq)
    
    return acquisition

    if acquisition:
    #    acquisition.pop('_id')
        return acquisition
    
    raise HTTPException(status_code=404,
        detail=f'Acquisition {acquisition_id} for specimen {specimen_id} not found')

@router.get('/acquisition/{acquisition_id}',
    tags=['acquisitions'])
def query_acquisition(acquisition_id: str,
                      query: dict):
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
            return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                content=updated_acquisition)
        
    raise HTTPException(status_code=404,
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
        
    raise HTTPException(status_code=404,
        detail=f'Acquisition {acquisition_id} not found')

# TODO: confirm data location stuff and 
@router.patch('/acquisition/{acquisition_id}',
    tags=['acquisitions'])
def patch_acquisition_status(acquisition_id: str,
                             status: str):
    update_result = dispimdb['acquisitions'].update_one({
        'acquisition_id': acquisition_id
    }, {'$set': {'data_location': status}})

    updated_acquisition = dispimdb['acquisitions'].find_one({
        'acquisition_id': acquisition_id
    })

    if update_result.modified_count == 1 and updated_acquisition:
        updated_acquisition.pop('_id')
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
            content=updated_acquisition)

    raise HTTPException(status_code=404,
        detail=f'Acquisition {acquisition_id} not found')

@router.delete('/acquisition/{acquisition_id}',
    tags=['acquisitions'])
def delete_acquisition(acquisition_id: str):
    delete_result = dispimdb['acquisitions'].delete_many({
        'acquisition_id': acquisition_id
    })

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
        
    raise HTTPException(status_code=404,
        detail=f'Acquisition {acquisition_id} not found')