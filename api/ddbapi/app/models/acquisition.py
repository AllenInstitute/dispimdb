from datetime import datetime
from typing import Optional, Dict

from pydantic import BaseModel, Field


class DataLocationModel(BaseModel):
    status: Optional[str]
    uri: str = Field(...)
    metadata: Optional[dict] = Field({})


class StartAcquisitionModel(BaseModel):
    section_num: str = Field(...)
    session_id: str = Field(...)
    specimen_id: str = Field(...)
    scope: str = Field(...)
    data_location: Optional[Dict[str, DataLocationModel]] = Field({})
    acquisition_metadata: Optional[dict] = Field({})
    acquisition_time_utc: datetime = Field(...)
    qc_state: Optional[str]

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
