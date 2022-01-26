from fastapi import APIRouter

from ddbapi.db.db import dispimdb_mongo
from ddbapi.app.utils import AppJSONResponse

router = APIRouter()


@router.get("/specimen/{specimen_id}/sections",
            tags=["sections"])
def get_sections(specimen_id: str):
    section_dicts = dispimdb_mongo.find_list(
        "sections", {
            "specimen_id": specimen_id})
    return AppJSONResponse(
        status_code=200,
        content=section_dicts)


@router.get("/specimen/{specimen_id}/section/{section_num}",
            tags=["sections"])
# FIxME section_num should be an int, but is not constrained in webapp
def get_section(specimen_id: str, section_num: str):
    section_dict = dispimdb_mongo.find_one(
       "sections", {"specimen_id": specimen_id,
                    "section_num": section_num})
    return AppJSONResponse(
        status_code=200,
        content=section_dict)
