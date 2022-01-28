from fastapi import APIRouter

from ddbapi.db.db import dispimdb_mongo
from ddbapi.app.utils import AppJSONResponse

router = APIRouter()


@router.get("/specimen/{specimen_id}/sessions",
            tags=["sessions"])
def get_sessions(specimen_id: str):
    session_dicts = dispimdb_mongo.find_list(
        "sessions", {
            "specimen_id": specimen_id})
    return AppJSONResponse(
        status_code=200,
        content=session_dicts)


@router.get("/specimen/{specimen_id}/session/{session_id}",
            tags=["sessions"])
def get_session(specimen_id: str, session_id: str):
    session_dict = dispimdb_mongo.find_one(
       "sessions", {"specimen_id": specimen_id,
                    "session_id": session_id})
    return AppJSONResponse(
        status_code=200,
        content=session_dict)
