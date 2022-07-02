from typing import List, Optional

from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from baking.database.core import Base
from baking.models import NameStr, OurBase, PrimaryKey
from baking.models import ProcedureMixin
from sqlalchemy.sql.schema import ForeignKey
from pydantic import Field
from .enums import IngrediantUnits, IngrediantType

############################################################
# SQL models...
############################################################


class Ingredient(Base, ProcedureMixin):
    """
    for example: water, 30, grams, flour
    """

    id = Column(Integer, primary_key=True)
    name = Column(String)
    quantity = Column(Integer)
    units = Column(String, default=IngrediantUnits.grams)
    type = Column(String, default=IngrediantType.Other)



############################################################
# Pydantic models...
############################################################
class IngredientBase(OurBase):
    name: NameStr
    quantity: Optional[int] = Field(1, gt=0, lt=100000)
    units: Optional[IngrediantUnits] = IngrediantUnits.grams
    type: Optional[IngrediantType] = IngrediantType.Other


class IngredientRead(IngredientBase):
    id: PrimaryKey


class IngredientCreate(IngredientBase):
    id: Optional[PrimaryKey]
    name: NameStr
    quantity: int = Field(1, gt=0, lt=100000)
    units: IngrediantUnits
    type: IngrediantType


class IngredientUpdate(IngredientBase):
    pass


class IngredientPagination(OurBase):
    total: int
    ingredients: List[IngredientBase] = []
