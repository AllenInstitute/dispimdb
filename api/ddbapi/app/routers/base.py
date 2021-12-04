from typing import Any, Dict

import fastapi
import fastapi.responses
import fastapi.encoders

import pymongo

from ddbapi.db.db import dispimdb

router = fastapi.APIRouter()


@router.put("/query/{collection}")
def query_collection(collection: str, request: Dict[Any, Any]):
    # TODO marshal this using pydantic
    allowed_keys = {
        "filter", "projection", "skip", "limit", "sort",
        "allow_partial_results",
        # "batch_size",
        "return_key", "show_record_id", "max_time_ms", "comment"}

    j = request

    sanitized_j = {k: j[k] for k in j.keys() & allowed_keys}

    try:
        curs = dispimdb[collection].find(**sanitized_j)
        # TODO optionally encode using ujson
        return fastapi.responses.JSONResponse(
            status_code=200,
            content=[*curs])
    except pymongo.errors.ExecutionTimeout:
        return fastapi.HTTPException(
            status_code=500,
            detail="querying timed out. query dict: {}".format(sanitized_j))
