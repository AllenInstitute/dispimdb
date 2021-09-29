import datetime

from pydantic import BaseModel, Field
from pydantic.fields import SHAPE_DEFAULTDICT
from typing import Optional

class SessionModel(BaseModel):
    session_id: str = Field(...)
    specimen_id: str = Field(...)
    section_num: int = Field(...)
    imaging_date: str = Field(...)
    scope: str = Field(...)
    objective: str = Field(...)
    objective_angle: str = Field(...)
    imaging_bath: str = Field(...)
    laser_power: str = Field(...)
    notes: str = Field(...)    

    class Config:
        schema_extra = {
            'example': {

            }
        }

class UpdateSessionModel(BaseModel):
    session_id: Optional[str]
    specimen_id: Optional[str]
    section_num: Optional[int]
    imaging_date: Optional[str]
    scope: Optional[str]
    objective: Optional[str]
    objective_angle: Optional[str]
    imaging_bath: Optional[str]
    laser_power: Optional[str]
    notes: Optional[str]