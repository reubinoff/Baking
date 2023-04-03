import pymongo
from enum import Enum
from datetime import datetime

from pydantic import BaseModel, HttpUrl
from pydantic.types import conint, constr


########################## SQLAlchemy models ##########################


class RecipeMixin(object):
    """Recipe mixin"""

    @declared_attr
    def recipe_id(cls):  # noqa
        return Column(Integer, ForeignKey("recipe.id", ondelete="CASCADE"))

    @declared_attr
    def recipe(cls):  # noqa
        return relationship("Recipe")


class ProcedureMixin(object):
    """Procedure mixin"""

    @declared_attr
    def procedure_id(cls):  # noqa
        return Column(Integer, ForeignKey("procedure.id", ondelete="CASCADE"))

    @declared_attr
    def procedure(cls):  # noqa
        return relationship("Procedure")

class TimeStampMixin(object):
    """Timestamping mixin"""

    created_at = Column(DateTime, default=datetime.utcnow)
    created_at._creation_order = 9998
    updated_at = Column(DateTime, default=datetime.utcnow)
    updated_at._creation_order = 9998

    @staticmethod
    def _updated_at(mapper, connection, target):
        target.updated_at = datetime.utcnow()

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, "before_update", cls._updated_at)


#################################################################

PrimaryKey = conint(gt=0, lt=2147483647)
NameStr = constr(regex=r"^(?!\s*$).+", strip_whitespace=True, min_length=3)

########################## Pydantic models ##########################


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
