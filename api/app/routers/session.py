from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from typing import Optional, List

from starlette.status import HTTP_201_CREATED

from db.db import dispimdb

from app.models.session import (
    SessionModel,
    UpdateSessionModel
)

router = APIRouter()

@router.post('/new_session',
    tags=['sessions'])
def create_session(session: SessionModel = Body(...)):
    session = jsonable_encoder(session)
    new_session = dispimdb['sessions'].insert_one(session)

    created_session = dispimdb['sessions'].find_one({
        '_id': new_session.inserted_id
    })
    created_session.pop('_id')

    return JSONResponse(status_code=HTTP_201_CREATED,
        content=created_session)

@router.get('/{specimen_id}/sessions',
    tags=['sessions'])
def get_sessions(specimen_id: str):
    sessions = []
    session_cursor = dispimdb['sessions'].find({
        'specimen_id': specimen_id
    })

    for session in session_cursor:
        session.pop('_id')
        sessions.append(session)
    
    if sessions:
        return sessions
    
    raise HTTPException(status_code=404,
        detail=f'No sessions found for specimen {specimen_id}')

@router.get('/{specimen_id}/session/{session_id}',
    tags=['sessions'])
def get_session(specimen_id: str,
                session_id: str):
    session = dispimdb['sessions'].find_one({
        'specimen_id': specimen_id,
        'session_id': session_id})

    if session:
        session.pop('_id')
        return session
    
    raise HTTPException(status_code=404,
        detail=f'Session {session_id} for specimen {specimen_id} not found')

@router.put('/{specimen_id}/session/{session_id}',
    tags=['sessions'])
def update_session(specimen_id: str,
                   session_id: str,
                   session: UpdateSessionModel = Body(...)):
    session = {k: v for k, v in session.dict().items() if v is not None}
    
    if len(session) >= 1:
        update_result = dispimdb['sessions'].update_one({
            'specimen_id': specimen_id,
            'session_id': session_id
        }, {'$set': session})

        updated_session = dispimdb['sessions'].find_one({
            'specimen_id': specimen_id,
            'session_id': session_id
        })

        if update_result.modified_count == 1 and updated_session:
            updated_session.pop('_id')
            return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                content=updated_session)
        
    raise HTTPException(status_code=404,
        detail=f'Session {session_id} for specimen {specimen_id} not found')

@router.delete('/{specimen_id}/session/{session_id}',
    tags=['sessions'])
def delete_session(specimen_id: str,
                   session_id: str):
    delete_result = dispimdb['sessions'].delete_one({
        'specimen_id': specimen_id,
        'session_id': session_id
    })

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    
    raise HTTPException(status_code=404,
        detail=f'Session {session_id} for specimen {specimen_id} not found')