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

# from baking.routers.procedure.models import Procedure, ProcedureCreate

# from baking.routers.users.models import User, UserRead


############################################################
# SQL models...
############################################################
class Recipe(Base, TimeStampMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    description = Column(String(50))

    # auther of the recipe ###############################################################
    # public = Column(Boolean)
    # user_id = Column(Integer, ForeignKey("user.id"), index=True, nullable=False)
    ###########################################################################################

    # procedures = relationship("Procedure", lazy="joined")
    ingredients = relationship(
        "Ingredient",
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
    name: str
    description: Optional[str]


class RecipeRead(RecipeBase):
    id: Optional[int]
    ingredients: List[IngredientCreate]


class RecipeCreate(RecipeBase):
    ingredients: Optional[List[IngredientCreate]]
    # procedures = List[ProcedureCreate]

    # user_id = Optional[UserRead]
    pass


class RecipeUpdate(RecipeBase):
    pass


class RecipePagination(OurBase):
    total: int
    recipes: List[RecipeBase] = []
