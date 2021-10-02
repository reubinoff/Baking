from typing import List, Optional

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    PrimaryKeyConstraint,
    String,
    Table,
    Boolean,
    DateTime,
)
from sqlalchemy.orm import relationship
from baking.database.core import Base
from baking.models import OurBase, TimeStampMixin


############################################################
# SQL models...
############################################################
class User(Base, TimeStampMixin):
    """ """

    id = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False)

    recipes = relationship("Recipe", backref="user")


############################################################
# Pydantic models...
############################################################
class RecipeBase(OurBase):
    name: str
    description: Optional[str]


class RecipeRead(RecipeBase):
    id: Optional[int]


class ItemCreate(RecipeBase):
    pass


class ItemPagination(OurBase):
    total: int
    items: List[RecipeBase] = []
