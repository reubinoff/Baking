from typing import List, Optional
from baking.models import NameStr, RecipeMixin
from pydantic import Field

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
    name = Column(String)
    description = Column(String)
    order = Column(Integer)

    ingredients = relationship(
        "Ingredient",
        lazy="subquery",
        cascade="all, delete-orphan",
        back_populates="procedure",
    )


############################################################
# Pydantic models...
############################################################
class ProcedureBase(OurBase):
    name: NameStr
    description: Optional[str] = Field(None, nullable=True)
    order: Optional[int] = Field(1)

    ingredients: Optional[List[IngredientCreate]]


class ProcedureRead(ProcedureBase):
    id: int


class ProcedureCreate(ProcedureBase):
    pass


class ProcedureUpdate(ProcedureBase):
    pass
