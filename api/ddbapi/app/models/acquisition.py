from pydantic import BaseModel, Field
from typing import Optional


class StartAcquisitionModel(BaseModel):
    section_num: int = Field(...)
    session_id: str = Field(...)
    specimen_id: str = Field(...)
    scope: str = Field(...)
    data_location: dict = Field(...)
    acquisition_metadata: dict = Field(...)
    acquisition_time_utc: str = Field(...)

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
