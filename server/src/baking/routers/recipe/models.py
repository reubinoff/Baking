from datetime import datetime
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
from sqlalchemy.ext.hybrid import hybrid_property

from baking.database.core import Base
from baking.models import OurBase, TimeStampMixin
from baking.routers.ingredients.enums import IngrediantType
from baking.routers.ingredients.models import (
    Ingredient,
    IngredientCreate,
    IngredientRead,
)

from baking.routers.procedure.models import Procedure, ProcedureCreate

# from baking.routers.users.models import User, UserRead


############################################################
# SQL models...
############################################################
class Recipe(Base, TimeStampMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    description = Column(String(100))

    # auther of the recipe ###############################################################
    # public = Column(Boolean)
    # user_id = Column(Integer, ForeignKey("user.id"), index=True, nullable=False)
    ###########################################################################################

    procedures = relationship(
        "Procedure",
        lazy="subquery",
        cascade="all, delete-orphan",
        back_populates="recipe",
    )
    # @hybrid_property
    # def hydration(self) -> int:
    #     water = None
    #     flour = None
    #     if self.ingredients:
    #         i: Ingredient = None
    #         for i in self.ingredients:
    #             if i.type == IngrediantType.water:
    #                 water = i.quanity
    #             elif i.type == IngrediantType.flour:
    #                 flour = i.quanity
    #         if water and flour:
    #             return (water / flour) * 100
    #     return -1


############################################################
# Pydantic models...
############################################################
class RecipeBase(OurBase):
    name: Optional[str]
    description: Optional[str]


class RecipeRead(RecipeBase):
    id: int
    procedures: Optional[List[ProcedureCreate]]


class RecipeCreate(RecipeBase):
    name: str
    procedures: Optional[List[ProcedureCreate]]


class RecipeUpdate(RecipeBase):
    pass


class RecipePagination(OurBase):
    total: int
    itemsPerPage: int
    page: int
    recipes: List[RecipeRead] = []
