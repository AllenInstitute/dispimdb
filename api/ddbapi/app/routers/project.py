from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from typing import Optional, List

from starlette.status import HTTP_201_CREATED

from ddbapi.db.db import dispimdb
from ddbapi.app.models.project import (
    ProjectModel,
    UpdateProjectModel
)

router = APIRouter()

@router.post('/new_project',
    tags=['projects'])
def create_project(project: ProjectModel = Body(...)):
    project = jsonable_encoder(project)
    new_project = dispimdb['projects'].insert_one(project)

    created_project = dispimdb['projects'].find_one({
        '_id': new_project.inserted_id
    })
    created_project.pop('_id')

    return JSONResponse(status_code=HTTP_201_CREATED,
        content=created_project)

@router.get('/projects',
    tags=['projects'])
def get_projects():
    projects = []
    project_cursor = dispimdb['projects'].find()

    for project in project_cursor:
        project.pop('_id')
        projects.append(project)
    
    if projects:
        return projects
    
    raise HTTPException(status_code=404,
        detail='No projects found')

@router.get('/project/{project_id}',
    tags=['projects'])
def get_project(project_id: str):
    project = dispimdb['projects'].find_one({
        'project_id': project_id
    })
    project.pop('_id')

    if project:
        return project
    
    raise HTTPException(status_code=404,
        detail=f'Project {project_id} not found')

@router.put('/project/{project_id}',
    tags=['projects'])
def update_project(project_id: str,
                    project: UpdateProjectModel = Body(...)):
    project = {k: v for k, v in project.dict().items() if v is not None}

    if len(project) >= 1:
        update_result = dispimdb['projects'].update_one({
            'project_id': project_id
        }, {'$set': project})
        
        updated_project = dispimdb['projects'].find_one({
            'project_id': project_id
        })

        if update_result.modified_count == 1 and updated_project:
            return updated_project
        
        raise HTTPException(status_code=404,
            detail=f'Project {project_id} not found')

@router.delete('/project/{project_id}',
    tags=['projects'])
def delete_project(project_id: str):
    delete_result = dispimdb['projects'].delete_one({
        'project_id': project_id
    })

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    
    raise HTTPException(status_code=404,
        detail=f'Project {project_id} not found')

