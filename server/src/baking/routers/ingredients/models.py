from typing import List, Optional

from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from baking.database.core import Base
from baking.models import OurBase
from baking.models import RecipeMixin
from sqlalchemy.sql.schema import ForeignKey

from .enums import IngrediantUnits, IngrediantType

############################################################
# SQL models...
############################################################


class Ingredient(Base, RecipeMixin):
    """
    for example: water, 30, grams
    """

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    quantity = Column(Integer)
    units = Column(String(32), default=IngrediantUnits.grams)
    type = Column(String(32), default=IngrediantType.Other)

    # procedure_id = Column(
    #     Integer, ForeignKey("procedure.id"), index=True, nullable=True
    # )


############################################################
# Pydantic models...
############################################################
class IngredientBase(OurBase):
    name: Optional[str]
    quantity: Optional[int]
    units: Optional[IngrediantUnits] = IngrediantUnits.grams
    type: Optional[IngrediantType] = IngrediantType.Other


class IngredientRead(IngredientBase):
    id: Optional[int]
    # procedure_id: Optional[int]


class IngredientCreate(IngredientBase):
    name: str
    quantity: int
    units: IngrediantUnits
    type: IngrediantType


class IngredientUpdate(IngredientBase):
    pass


class IngredientPagination(OurBase):
    total: int
    ingredients: List[IngredientBase] = []
