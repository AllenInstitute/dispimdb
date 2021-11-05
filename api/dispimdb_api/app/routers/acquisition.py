import os
from datetime import datetime

from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from typing import Optional, List
from starlette.status import HTTP_201_CREATED

from dispimdb_api.db.db import dispimdb
from dispimdb_api.app.models.acquisition import (
    StartAcquisitionModel,
    UpdateAcquisitionModel
)

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

@router.get('/{specimen_id}/acquisition/{acquisition_id}',
    tags=['acquisitions'])
def get_acquisition(specimen_id: str,
                    acquisition_id: str):
    #acquisition = dispimdb['acquisitions'].find_one({
    #    'specimen_id': specimen_id,
    #    'acquisition_id': acquisition_id})
    acquisition = []
    acq_cursor = dispimdb['acquisitions'].find({
        'specimen_id': specimen_id,
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

@router.put('/{specimen_id}/acquisition/{acquisition_id}',
    tags=['acquisitions'])
def update_acquisition(specimen_id: str,
                       acquisition_id: str, 
                       acquisition: UpdateAcquisitionModel = Body(...)):
    acquisition = {k: v for k, v in acquisition.dict().items() if v is not None}
    
    if len(acquisition) >= 1:
        update_result = dispimdb['acquisitions'].update_one({
            'specimen_id': specimen_id,
            'acquisition_id': acquisition_id
        }, {'$set': acquisition})

        updated_acquisition = dispimdb['acquisitions'].find_one({
            'specimen_id': specimen_id,
            'acquisition_id': acquisition_id
        })

        if update_result.modified_count == 1 and updated_acquisition:
            updated_acquisition.pop('_id')
            return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                content=updated_acquisition)
        
    raise HTTPException(status_code=404,
        detail=f'Acquisition {acquisition_id} for specimen {specimen_id} not found')

@router.patch('/{specimen_id}/acquisition/{acquisition_id}',
    tags=['acquisitions'])
def patch_acquisition(specimen_id: str,
                      acquisition_id: str,
                      data: dict):
    
    if len(data) >= 1:
        update_result = dispimdb['acquisitions'].update_one({
            'specimen_id': specimen_id,
            'acquisition_id': acquisition_id
        }, {'$set': data})

        updated_acquisition = dispimdb['acquisitions'].find_one({
            'specimen_id': specimen_id,
            'acquisition_id': acquisition_id
        })

        if update_result.modified_count == 1 and updated_acquisition:
            updated_acquisition.pop('_id')
            return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                content=updated_acquisition)
        
    raise HTTPException(status_code=404,
        detail=f'Acquisition {acquisition_id} for specimen {specimen_id} not found')

@router.delete('/{specimen_id}/acquisition/{acquisition_id}',
    tags=['acquisitions'])
def delete_acquisition(specimen_id: str,
                       acquisition_id: str):
    delete_result = dispimdb['acquisitions'].delete_many({
        'specimen_id': specimen_id,
        'acquisition_id': acquisition_id
    })

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
        
    raise HTTPException(status_code=404,
        detail=f'Acquisition {acquisition_id} for specimen {specimen_id} not found')

@router.get('/{specimen_id}/acquisition/{acquisition_id}/list_contents',
    tags=['acquisitions'])
def list_acquisition_contents(specimen_id: str,
                              acquisition_id: str):
    acquisition = dispimdb['acquisitions'].find_one({
        'specimen_id': specimen_id,
        'acquisition_id': acquisition_id})
    acquisition.pop('_id')

    mount_dir = '/'

    if acquisition['scope'] == 'ispim1':
        mount_dir += 'ispim1_data'
    elif acquisition['scope'] == 'ispim2':
        mount_dir += 'ispim2_data'
    
    acquisition_dir = os.path.join(mount_dir, acquisition['data_location']['tiff_directory'])
    dir_contents = os.listdir(acquisition_dir)

    if dir_contents:
        return dir_contents
    
    raise HTTPException(status_code=404,
        detail=f'Directory for acquisition {acquisition_id} with specimen {specimen_id} not found')

@router.get('/{specimen_id}/acquisition/{acquisition_id}/get_overview',
    tags=['acquisitions'])
def get_acquisition_overview(specimen_id: str,
                             acquisition_id: str):
    acquisition = dispimdb['acquisitions'].find_one({
        'specimen_id': specimen_id,
        'acquisition_id': acquisition_id})
    acquisition.pop('_id')

    mount_dir = '/'

    if acquisition['scope'] == 'ispim1':
        mount_dir += 'ispim1_data'
    elif acquisition['scope'] == 'ispim2':
        mount_dir += 'ispim2_data'
    
    acquisition_dir = os.path.join(mount_dir, acquisition['data_location']['tiff_directory'])
    overview_path = os.path.join(acquisition_dir, 'overview.gif')

    return FileResponse(overview_path)

@router.get('/{specimen_id}/acquisition/{acquisition_id}/get_block',
    tags=['acquisitions'])
def get_acquisition_block(specimen_id: str,
                          acquisition_id: str):
    acquisition = dispimdb['acquisitions'].find_one({
        'specimen_id': specimen_id,
        'acquisition_id': acquisition_id})
    acquisition.pop('_id')

    mount_dir = '/'

    if acquisition['scope'] == 'ispim1':
        mount_dir += 'ispim1_data'
    elif acquisition['scope'] == 'ispim2':
        mount_dir += 'ispim2_data'
    
    acquisition_dir = os.path.join(mount_dir, acquisition['data_location']['tiff_directory'])

    return {}

@router.get('/{specimen_id}/acquisition/{acquisition_id}/get_strip/{strip_num}',
    tags=['acquisitions'])
def get_acquisition_strip(specimen_id: str,
                          acquisition_id: str):
    acquisition = dispimdb['acquisitions'].find_one({
        'specimen_id': specimen_id,
        'acquisition_id': acquisition_id})
    acquisition.pop('_id')

    mount_dir = '/'

    if acquisition['scope'] == 'ispim1':
        mount_dir += 'ispim1_data'
    elif acquisition['scope'] == 'ispim2':
        mount_dir += 'ispim2_data'
    
    acquisition_dir = os.path.join(mount_dir, acquisition['data_location']['tiff_directory'])

    return {}

@router.get('/{specimen_id}/acquisition/{acquisition_id}/get_segment/{strip_num}/{segment_num}',
    tags=['acquisitions'])
def get_acquisition_segment(specimen_id: str,
                          acquisition_id: str):
    return {}
