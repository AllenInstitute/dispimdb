from fastapi import APIRouter

from ddbapi.db.db import dispimdb_mongo
from ddbapi.app.utils import AppJSONResponse

router = APIRouter()


@router.get("/specimens",
            tags=["specimens"])
def get_specimens():
    specimen_dicts = dispimdb_mongo.find_list(
        "specimens", {})
    return AppJSONResponse(
        status_code=200,
        content=specimen_dicts)


@router.get("/specimen/{specimen_id}",
            tags=["specimens"])
def get_specimen(specimen_id: str):
    specimen_dict = dispimdb_mongo.find_one(
       "specimens", {"specimen_id": specimen_id})
    return AppJSONResponse(
        status_code=200,
        content=specimen_dict)
