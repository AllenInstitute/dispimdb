import datetime
import os
from typing import Dict, Any

from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_201_CREATED

import pymongo

from dispimdb_api.db.db import dispimdb
from dispimdb_api.app.models.acquisition import (
    StartAcquisitionModel,
    UpdateAcquisitionModel
)

router = APIRouter()

# TODO define indices
acquisition_indices = []


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


# TODO this should probably just post to /acquisition
@router.post('/new_acquisition',
             tags=['acquisitions'])
def create_acquisition(acquisition: StartAcquisitionModel = Body(...)):
    acquisition = jsonable_encoder(acquisition)
    acquisition = acquisition_with_id(acquisition)
    acq_insert = dispimdb['acquisitions'].insert_one(acquisition)
    # don't assert....
    assert acq_insert.inserted_id == acquisition["_id"]

    # created_acquisition = dispimdb['acquisitions'].find_one({
    #     '_id': new_acquisition.inserted_id
    # })
    # created_acquisition.pop('_id')

    if acquisition_indices:
        dispimdb["acquisitions"].create_indexes(
            acquisition_indices)

    return JSONResponse(
        status_code=HTTP_201_CREATED,
        content=acquisition)


@router.get('/{specimen_id}/acquisitions',
    tags=['acquisitions'])
def get_acquisitions(specimen_id: str):
    acquisitions = []
    acquisition_cursor = dispimdb['acquisitions'].find({
        'specimen_id': specimen_id
    })

    for acquisition in acquisition_cursor:
        acquisition.pop('_id')
        acquisitions.append(acquisition)

    if acquisitions:
        return acquisitions

    raise HTTPException(status_code=404,
        detail=f'No acquisitions found for specimen {specimen_id}')

@router.get('/{specimen_id}/acquisition/{acquisition_id}',
    tags=['acquisitions'])
def get_acquisition(specimen_id: str,
                    acquisition_id: str):
    acquisition = dispimdb['acquisitions'].find_one({
        'specimen_id': specimen_id,
        'acquisition_id': acquisition_id})

    if acquisition:
        acquisition.pop('_id')
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

@router.delete('/{specimen_id}/acquisition/{acquisition_id}',
    tags=['acquisitions'])
def delete_acquisition(specimen_id: str,
                       acquisition_id: str):
    delete_result = dispimdb['acquisitions'].delete_one({
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
    raise NotImplementedError
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
    raise NotImplementedError
    return {}

@router.get('/{specimen_id}/acquisition/{acquisition_id}/get_segment/{strip_num}/{segment_num}',
    tags=['acquisitions'])
def get_acquisition_segment(specimen_id: str,
                          acquisition_id: str):
    raise NotImplementedError
    return {}


@router.patch('/acquisitions/{acquisition_id}/data_location/{data_key}/status/{state}',
              tags=["acquisitions"])
def patch_data_location_status(acquisition_id: str, data_key: str,
                               state: str):
    # TODO implement state table w/ allowed transitions
    update_field = f"data_location.{data_key}.status"
    updated_doc = dispimdb["acquisitions"].find_one_and_update(
      {"_id": acquisition_id},
      {"$set": {update_field: state}},
      return_document=pymongo.ReturnDocument.AFTER
    )
    return JSONResponse(status_code=200)


@router.put("/acquisitions/{acquisition_id}/data_location/{data_key}",
            tags=["acquisitions"])
def put_data_location(acquisition_id: str, data_key: str,
                      request: Dict[Any, Any]):
    # TODO do not allow overwriting
    # TODO
    update_field = f"data_location.{data_key}"
    updated_doc = dispimdb["acquisitions"].find_one_and_update(
         {"_id": acquisition_id},
         {"$set": {update_field: request}},
         return_document=pymongo.ReturnDocument.AFTER
    )
    return JSONResponse(status_code=200)
