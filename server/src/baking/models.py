from datetime import datetime

from pydantic import BaseModel, HttpUrl
from pydantic.types import conint, constr

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, DateTime, Integer, event, ForeignKey
from sqlalchemy.orm import relationship

from baking.database.filters.filters import Operator
########################## SQLAlchemy models ##########################


class RecipeMixin(object):
    """Recipe mixin"""

    @declared_attr
    def recipe_id(cls):  # noqa
        return Column(Integer, ForeignKey("recipe.id", ondelete="CASCADE"))

    @declared_attr
    def recipe(cls):  # noqa
        return relationship("Recipe")


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
NameStr = constr(regex=r"^(?!\s*$).+", strip_whitespace=True, min_length=4)

########################## Pydantic models ##########################
class OurBase(BaseModel):
    class Config:
        orm_mode = True
        validate_assignment = True
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True

        json_encoders = {
            # custom output conversion for datetime
            datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%SZ")
            if v
            else None
        }


class FileUploadData(BaseModel):
    url: HttpUrl
    identidier: str


class FilterObject(BaseModel):
    model: str
    field: str
    op: str
    value: str
#################################################################
