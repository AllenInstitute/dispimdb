import datetime

from pydantic import BaseModel, Field
from typing import Optional

class SpecimenModel(BaseModel):
    specimen_id: str = Field(...)
    project_id: str = Field(...)
    pedigree: str = Field(...)
    sex: str = Field(...)
    dob: str = Field(...)
    perfusion_date: str = Field(...)
    perfusion_age: int = Field(...)
    perfusion_notes: str = Field(...)
    experiment: str = Field(...)
    status: str = Field(...)
    notes: str = Field(...)

    class Config:
        schema_extra = {
            'example': {

            }
        }

class UpdateSpecimenModel(BaseModel):
    specimen_id: Optional[str]
    project_id: Optional[str]
    pedigree: Optional[str]
    sex: Optional[str]
    dob: Optional[str]
    perfusion_date: Optional[str]
    perfusion_age: Optional[int]
    perfusion_notes: Optional[str]
    experiment: Optional[str]
    status: Optional[str]
    notes: Optional[str]