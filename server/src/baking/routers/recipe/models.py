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
class Item(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    description = Column(String(50))


############################################################
# Pydantic models...
############################################################
class ItemBase(OurBase):
    name: str
    description: Optional[str]


class ItemRead(ItemBase):
    id: Optional[int]


class ItemCreate(ItemBase):
    pass


class ItemPagination(OurBase):
    total: int
    items: List[ItemRead] = []
