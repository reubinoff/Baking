import pymongo
from typing import Annotated
from enum import Enum
from datetime import datetime
from bson.objectid import ObjectId
from pydantic import BaseModel, HttpUrl, constr, conint


from pydantic.fields import Field


NameStr = constr(regex=r"^(?!\s*$).+", strip_whitespace=True, min_length=3)
PrimaryKey = constr(strip_whitespace=True)
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")
    


class BakingBaseModel(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    _encoders_by_type = {datetime: lambda dt: dt.isoformat(timespec='seconds')}

    def _iter(self, **kwargs):
        for key, value in super()._iter(**kwargs):
            yield key, self._encoders_by_type.get(type(value), lambda v: v)(value)
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

class FileUploadData(BaseModel):
    url: HttpUrl
    identifier: str


class SortOrder(str, Enum):
    ASCENDING = pymongo.ASCENDING
    DESCENDING = pymongo.DESCENDING

class FilterOperator(str, Enum):
    CONTAINS = "$regex"
    EQUALS = "$eq"
    GREATER_THAN = "$gt"
    GREATER_THAN_OR_EQUAL = "$gte"
    LESS_THAN = "$lt"
    LESS_THAN_OR_EQUAL = "$lte"


class FilterCriteria(BaseModel):
    # name mak length 3 chars
    name: str = Field(..., min_length=1, max_length=20)
    value: str = Field(..., min_length=1, max_length=50)
    operator: FilterOperator = Field(..., min_length=1, max_length=50)
#################################################################
