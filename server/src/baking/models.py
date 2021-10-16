from datetime import datetime, timedelta

from pydantic import BaseModel, validator
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Boolean, Column, DateTime, Integer, String, event, ForeignKey
from sqlalchemy.orm import relationship

########################## SQLAlchemy models ##########################


class RecipeMixin(object):
    """Recipe mixin"""

    @declared_attr
    def recipe_id(cls):  # noqa
        return Column(
            Integer,
            ForeignKey("recipe.id", ondelete="CASCADE"),
            index=True,
            nullable=False,
        )

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


########################## Pydantic models ##########################
class OurBase(BaseModel):
    class Config:
        orm_mode = True
        validate_assignment = True
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True


#################################################################
