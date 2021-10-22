from pydantic import BaseModel, Field
from typing import Optional

class ProjectModel(BaseModel):
    project_id: str = Field(...)
    
    class Config:
        schema_extra = {
            'example': {

            }
        }

class UpdateProjectModel(BaseModel):
    pass