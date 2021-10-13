from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from typing import Optional, List

from starlette.status import HTTP_201_CREATED

from api.db.db import dispimdb

from api.app.models.specimen import (
    SpecimenModel,
    UpdateSpecimenModel
)

router = APIRouter()

@router.post('/',
    tags=['specimens'])
def create_specimen(specimen: SpecimenModel = Body(...)):
    specimen = jsonable_encoder(specimen)
    new_specimen = dispimdb['specimens'].insert_one(specimen)

    created_specimen = dispimdb['specimens'].find_one({
        '_id': new_specimen.inserted_id
    })
    created_specimen.pop('_id')

    return JSONResponse(status_code=HTTP_201_CREATED,
        content=created_specimen)

@router.get('/',
    tags=['specimens'])
def get_specimens():
    specimens = []
    specimen_cursor = dispimdb['specimens'].find()

    for specimen in specimen_cursor:
        specimen.pop('_id')
        specimens.append(specimen)
    
    if specimens:
        return specimens
    
    raise HTTPException(status_code=404,
        detail='No specimens found')

@router.get('/{specimen_id}',
    tags=['specimens'])
def get_specimen(specimen_id: str):
    specimen = dispimdb['specimens'].find_one({
        'specimen_id': specimen_id
    })

    if specimen:
        specimen.pop('_id')
        return specimen
    
    raise HTTPException(status_code=404,
        detail=f'Specimen {specimen_id} not found')

@router.put('/{specimen_id}',
    tags=['specimens'])
def update_specimen(specimen_id: str,
                    specimen: UpdateSpecimenModel = Body(...)):
    specimen = {k: v for k, v in specimen.dict().items() if v is not None}

    if len(specimen) >= 1:
        update_result = dispimdb['specimens'].update_one({
            'specimen_id': specimen_id
        }, {'$set': specimen})
        
        updated_specimen = dispimdb['specimens'].find_one({
            'specimen_id': specimen_id
        })
        updated_specimen.pop('_id')

        if update_result.modified_count == 1 and updated_specimen:
            return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                content=updated_specimen)
        
        raise HTTPException(status_code=404,
            detail=f'Specimen {specimen_id} not found')

@router.delete('/{specimen_id}',
    tags=['specimens'])
def delete_specimen(specimen_id: str):
    delete_result = dispimdb['specimens'].delete_one({
        'specimen_id': specimen_id
    })

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    
    raise HTTPException(status_code=404,
        detail=f'Specimen {specimen_id} not found')

