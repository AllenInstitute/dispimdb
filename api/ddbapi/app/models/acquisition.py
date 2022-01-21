from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class StartAcquisitionModel(BaseModel):
    section_num: int = Field(...)
    session_id: str = Field(...)
    specimen_id: str = Field(...)
    scope: str = Field(...)
    data_location: Optional[dict] = Field({})
    acquisition_metadata: Optional[dict] = Field({})
    acquisition_time_utc: datetime = Field(...)

    class Config:
        schema_extra = {
            'example': {
            }
        }


class UpdateAcquisitionModel(BaseModel):
    acquisition_id: Optional[str]
    section_num: Optional[int]
    session_id: Optional[str]
    specimen_id: Optional[str]
    scope: Optional[str]
    acquisition_metadata: Optional[dict]
    data_location: Optional[dict]
    acquisition_time_utc: Optional[str]
