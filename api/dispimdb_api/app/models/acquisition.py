from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, Field


class StartAcquisitionModel(BaseModel):
    # acquisition_id: str = Field(...)
    section_num: int = Field(...)
    session_id: str = Field(...)
    specimen_id: str = Field(...)
    scope: str = Field(...)
    acquisition_time_utc: datetime = Field(...)
    acquisition_metadata: Optional[dict] = Field({})
    data_location: Optional[dict] = Field({})

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
