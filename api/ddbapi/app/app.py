import os
from typing import Optional

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from .routers import acquisition

api = FastAPI()

api.include_router(acquisition.router)
#api.include_router(project.router)
#api.include_router(section.router)
#api.include_router(session.router)
#api.include_router(specimen.router)

ENVIRON_ROOT_PATH = os.getenv("DISPIMDB_ROOT_PATH")
app = FastAPI(root_path=ENVIRON_ROOT_PATH)
app.mount('/api', api)
