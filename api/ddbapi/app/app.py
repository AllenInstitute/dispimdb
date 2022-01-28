import os

from fastapi import FastAPI

from .routers import acquisition

api = FastAPI()

api.include_router(acquisition.router)

ENVIRON_ROOT_PATH = os.getenv("DISPIMDB_ROOT_PATH")
app = FastAPI(root_path=ENVIRON_ROOT_PATH)
app.mount('/api', api)
