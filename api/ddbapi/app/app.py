import os

from fastapi import FastAPI

from .routers import (
    acquisition, specimen, section, session)

api = FastAPI()

api.include_router(acquisition.router)
api.include_router(specimen.router)
api.include_router(session.router)
api.include_router(section.router)

ENVIRON_ROOT_PATH = os.getenv("DISPIMDB_ROOT_PATH")
app = FastAPI(root_path=ENVIRON_ROOT_PATH)
app.mount('/api', api)
