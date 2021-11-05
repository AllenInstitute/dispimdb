from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from typing import Optional, List

from starlette.status import HTTP_201_CREATED

from dispimdb_api.db.db import dispimdb

from dispimdb_api.app.models.section import (
    SectionModel,
    UpdateSectionModel
)

router = APIRouter()

@router.post('/new_section',
    tags=['sections'])
def create_section(section: SectionModel = Body(...)):
    section = jsonable_encoder(section)
    new_section = dispimdb['sections'].insert_one(section)

    created_section = dispimdb['sections'].find_one({
        '_id': new_section.inserted_id
    })
    created_section.pop('_id')

    return JSONResponse(status_code=HTTP_201_CREATED,
        content=created_section)

@router.get('/{specimen_id}/sections',
    tags=['sections'])
def get_sections(specimen_id: str):
    sections = []
    section_cursor = dispimdb['sections'].find({
        'specimen_id': specimen_id
    })

    for section in section_cursor:
        section.pop('_id')
        sections.append(section['section_num'])
    
    if sections:
        return sections
    
    raise HTTPException(status_code=404,
        detail=f'No sections found for specimen {specimen_id}')

@router.get('/{specimen_id}/section/{section_num}',
    tags=['sections'])
def get_section(specimen_id: str,
                section_num: int):
    section = dispimdb['sections'].find_one({
        'specimen_id': specimen_id,
        'section_num': section_num})

    if section:
        section.pop('_id')
        return section
    
    raise HTTPException(status_code=404,
        detail=f'Section {section_num} for specimen {specimen_id} not found')

@router.put('/{specimen_id}/section/{section_num}',
    tags=['sections'])
def update_section(specimen_id: str,
                       section_num: int, 
                       section: UpdateSectionModel = Body(...)):
    section = {k: v for k, v in section.dict().items() if v is not None}
    
    if len(section) >= 1:
        update_result = dispimdb['sections'].update_one({
            'specimen_id': specimen_id,
            'section_num': section_num
        }, {'$set': section})

        updated_section = dispimdb['sections'].find_one({
            'specimen_id': specimen_id,
            'section_num': section_num
        })

        if update_result.modified_count == 1 and updated_section:
            updated_section.pop('_id')
            return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                content=updated_section)
        
    raise HTTPException(status_code=404,
        detail=f'Section {section_num} for specimen {specimen_id} not found')

@router.delete('/{specimen_id}/section/{section_num}',
    tags=['sections'])
def delete_section(specimen_id: str,
                   section_num: int):
    delete_result = dispimdb['sections'].delete_one({
        'specimen_id': specimen_id,
        'section_num': section_num
    })

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    
    raise HTTPException(status_code=404,
        detail=f'Section {section_num} for specimen {specimen_id} not found')
