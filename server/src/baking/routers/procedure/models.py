from typing import List, Optional
from baking.models import RecipeMixin

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from baking.database.core import Base
from baking.models import OurBase


############################################################
# SQL models...
############################################################
class Procedure(Base, RecipeMixin):
    """
    Procedure in the recipe
    """

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    position = Column(Integer)

    ingredients = relationship("Ingredient", backref="procedure")


############################################################
# Pydantic models...
############################################################
class ProcedureBase(OurBase):
    name: str
    description: Optional[str]


class ProcedureRead(ProcedureBase):
    id: Optional[int]


class ItemCreate(ProcedureBase):
    pass


class ItemPagination(OurBase):
    total: int
    items: List[ProcedureBase] = []
