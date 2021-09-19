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
from baking.database.core import Base
from baking.models import OurBase


############################################################
# SQL models...
############################################################
class Recipe(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    description = Column(String(50))


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
