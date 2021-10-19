from typing import List, Optional
from baking.models import RecipeMixin

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from baking.database.core import Base
from baking.models import OurBase

from baking.routers.ingredients.models import IngredientCreate

############################################################
# SQL models...
############################################################
class Procedure(Base, RecipeMixin):
    """
    Procedure in the recipe
    """

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    description = Column(String(100))
    order = Column(Integer)

    ingredients = relationship(
        "Ingredient",
        lazy="subquery",
        back_populates="procedure",
    )


############################################################
# Pydantic models...
############################################################
class ProcedureBase(OurBase):
    name: str
    description: Optional[str]
    order: Optional[int] = 1


class ProcedureRead(ProcedureBase):
    id: int
    name: str
    description: Optional[str]
    order: Optional[int]

    ingredients: Optional[List[IngredientCreate]]


class ProcedureCreate(ProcedureBase):
    ingredients: Optional[List[IngredientCreate]]


class ProcedureUpdate(ProcedureBase):
    pass
