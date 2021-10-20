from typing import List, Optional
from baking.models import NameStr, PrimaryKey, RecipeMixin
from pydantic import Field
from sqlalchemy.ext.hybrid import hybrid_property

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from baking.database.core import Base
from baking.models import OurBase

from baking.routers.ingredients.models import (
    Ingredient,
    IngredientCreate,
    IngredientRead,
)
from baking.routers.ingredients.enums import IngrediantType, is_liquid

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

    @hybrid_property
    def total_liquid(self) -> int:
        liquid = 0
        if self.ingredients is not None:
            i: Ingredient = None
            for i in self.ingredients:
                if is_liquid(i.type) is True:
                    liquid = liquid + i.quantity

        return liquid

    @hybrid_property
    def total_solid(self) -> int:
        solid = 0
        if self.ingredients is not None:
            i: Ingredient = None
            for i in self.ingredients:
                if is_liquid(i.type) is False:
                    solid = solid + i.quantity

        return solid

    @hybrid_property
    def procedure_hydration(self) -> int:
        if self.total_solid > 0:
            return int((self.total_liquid / self.total_solid) * 100)
        return 100  # precent hydration


############################################################
# Pydantic models...
############################################################
class ProcedureBase(OurBase):
    name: NameStr
    description: Optional[str] = Field(None, nullable=True)
    order: Optional[int] = Field(1, gt=0, lt=100)

    ingredients: Optional[List[IngredientRead]]


class ProcedureRead(ProcedureBase):
    id: PrimaryKey
    procedure_hydration: int


class ProcedureCreate(ProcedureBase):
    id: Optional[PrimaryKey]
    ingredients: Optional[List[IngredientCreate]] = []


class ProcedureUpdate(ProcedureBase):
    name: Optional[NameStr]
    ingredients: Optional[List[IngredientCreate]] = []


class ProcedurePagination(OurBase):
    total: int
    itemsPerPage: int
    page: int
    items: List[ProcedureRead] = []
