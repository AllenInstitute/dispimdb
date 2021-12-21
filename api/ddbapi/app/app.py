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

app = FastAPI()
app.mount('/api', api)