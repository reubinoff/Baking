import pymongo
from enum import Enum
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, HttpUrl, constr


from pydantic.fields import Field


NameStr = constr(regex=r"^(?!\s*$).+", strip_whitespace=True, min_length=3)


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
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

class FileUploadData(BaseModel):
    url: HttpUrl
    identidier: str


class FilterOperator(str, Enum):
    EQUALS = "equals"
    CONTAINS = "contains"
    GREATER_THAN = "gt"
    GREATER_THAN_OR_EQUAL = "gte"
    LESS_THAN = "lt"
    LESS_THAN_OR_EQUAL = "lte"


class FilterCriteria(BaseModel):
    name: str
    value: str
    operator: str = "equals"


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
#################################################################
