import pymongo
from typing import Annotated, Callable, Dict, List, Optional, Union
from enum import Enum
from bson.objectid import ObjectId
from pydantic import BaseModel, HttpUrl, constr, GetJsonSchemaHandler, field_serializer
from typing import Any
from pydantic_core import CoreSchema, core_schema
from pydantic.json_schema import JsonSchemaValue


from pydantic.fields import Field


NameStr = constr(pattern=r"^\S.*\S$", strip_whitespace=True, min_length=3)
PrimaryKey = constr(strip_whitespace=True)

class _PyObjectIdAnnotation:
    @classmethod
    def __get_pydantic_core_schema__(
            cls,
            _source_type: Any,
            _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:

        def validate_from_str(id_: str) -> ObjectId:
            return ObjectId(id_)

        from_str_schema = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(
                    validate_from_str),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_str_schema,
            python_schema=core_schema.union_schema(
                [
                    # check if it's an instance first before doing any further work
                    core_schema.is_instance_schema(ObjectId),
                    from_str_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: str(instance)
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
            cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        # Use the same schema that would be used for `str`
        return handler(core_schema.str_schema())

PyObjectId = Annotated[ObjectId, _PyObjectIdAnnotation()]

class BakingBaseModel(BaseModel):

    class ConfigDict:
        populate_by_name = True
        arbitrary_types_allowed = True

class FileUploadData(BaseModel):
    url: HttpUrl
    identifier: str

    @field_serializer('url')
    def serialize_created_at(self, url: HttpUrl, _info):
        return str(url)


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
