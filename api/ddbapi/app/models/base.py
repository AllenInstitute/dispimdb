import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class DispimDbBase(BaseModel):
    date_added: datetime.datetime = Field(...)
    added_by: datetime.datetime = Field(...)
    date_modified: datetime.datetime = Field(...)
    modified_by: datetime.datetime = Field(...)


class MongoQueryModel(BaseModel):
    filter: Optional[dict] = Field(None)
    projection: Optional[dict] = Field(None)
    skip: Optional[int] = Field(0)
    limit: Optional[int] = Field(0)
    sort: Optional[dict] = Field(None)
    allow_partial_results: Optional[bool] = Field(False)
    # batch_size
    return_key: Optional[bool] = Field(None)
    show_record_id: Optional[bool] = Field(None)
    max_time_ms: Optional[int] = Field(None)
    comment: Optional[str] = Field(None)
