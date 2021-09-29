from pydantic import BaseModel, Field
from typing import Optional

class SectionModel(BaseModel):
    section_num: int = Field(...)
    specimen_id: str = Field(...)
    cut_plane: str = Field(...)
    thickness: str = Field(...)
    prep_type: str = Field(...)
    fluorescent_labels: str = Field(...)
    other_notes: str = Field(...)

    class Config:
        schema_extra = {
            'example': {

            }
        }

class UpdateSectionModel(BaseModel):
    section_num: Optional[int]
    specimen_id: Optional[str]
    cut_plane: Optional[str]
    thickness: Optional[str]
    prep_type: Optional[str]
    fluorescent_labels: Optional[str]
    other_notes: Optional[str]