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
from baking.models import OurBase
from baking.models import RecipeMixin

from .enums import Units, IngrediantType

############################################################
# SQL models...
############################################################


class Ingredient(Base, RecipeMixin):
    """
    for example: water, 30, grams
    """

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    quanity = Column(Integer)
    units = Column(String(32), default=Units.grams)
    type = Column(String(32), default=IngrediantType.Other)

    procedure_id = Column(
        Integer, ForeignKey("procedure.id"), index=True, nullable=True
    )


############################################################
# Pydantic models...
############################################################
class IngredientBase(OurBase):
    name: str
    quantity: int
    units: Optional[Units] = Units.grams
    recipe_id: int
    type: Optional[IngrediantType] = IngrediantType.Other


class IngredientRead(IngredientBase):
    id: Optional[int]
    procedure_id: Optional[int]


class IngredientCreate(IngredientBase):
    pass


class IngredientPagination(OurBase):
    total: int
    ingredients: List[IngredientBase] = []
