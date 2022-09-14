import json
import os

import fastapi.middleware.cors


CORS_SETTINGS_ENV_VAR = "DISPIMDB_CORS_JSON"


def retrieve_CORS_options():
    try:
        cors_json = os.environ[CORS_SETTINGS_ENV_VAR]
    except KeyError:
        return None

    try:
        with open(cors_json, "r") as f:
            cors_options = json.load(f)
    except Exception:
        return None
    return cors_options

cors_options = retrieve_CORS_options()
include_CORS = cors_options is not None

CORSMiddleware = fastapi.middleware.cors.CORSMiddleware

__all__ = ["include_CORS", "CORSMiddleware", "cors_options"]