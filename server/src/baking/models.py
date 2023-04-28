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

    @classmethod
    def __str__(cls, v):
        return str(v)
        
    


class BakingBaseModel(BaseModel):

    @classmethod
    def get_properties(cls):
        return (
            prop for prop in dir(cls)
            if isinstance(getattr(cls, prop), property) and prop not in ("__values__", "fields")
        )

    _encoders_by_type = {
        datetime: lambda dt: dt.isoformat(timespec='seconds'),
        PyObjectId: lambda id: str(id),
        ObjectId: lambda id: str(id), 
        HttpUrl: lambda url: str(url)
    }

    def _iter(self, **kwargs):
        for key, value in super()._iter(**kwargs):
            yield key, self._encoders_by_type.get(type(value), lambda v: v)(value)

    @classmethod
    def get_properties(cls):
        return [prop for prop in dir(cls) if isinstance(getattr(cls, prop), property)]

    def dict(self, *args, **kwargs):
        self.__dict__.update(
            {prop: getattr(self, prop) for prop in self.get_properties()}
        )
        return super().dict(*args, **kwargs)

    def json(
        self,
        *args,
        **kwargs,
    ) -> str:
        self.__dict__.update(
            {prop: getattr(self, prop) for prop in self.get_properties()}
        )

        return super().json(*args, **kwargs)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

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
