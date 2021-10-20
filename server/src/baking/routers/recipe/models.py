from datetime import datetime
from typing import List, Optional
from pydantic import Field, validator

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
from baking.models import OurBase, PrimaryKey, TimeStampMixin, NameStr
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
    name = Column(String)
    description = Column(String)

    # auther of the recipe ###############################################################
    # public = Column(Boolean)
    # user_id = Column(Integer, ForeignKey("user.id"), index=True, nullable=False)
    ###########################################################################################

    procedures = relationship(
        "Procedure",
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
    name: Optional[NameStr]
    description: Optional[str] = Field(None, nullable=True)
    procedures: Optional[List[ProcedureCreate]]

    @validator("name")
    def title_required(cls, v):
        if not v or "\x00" in v:
            raise ValueError("must not be empty string")
        return v


class RecipeRead(RecipeBase):
    id: PrimaryKey
    name: NameStr


class RecipeCreate(RecipeBase):
    name: NameStr


class RecipeUpdate(RecipeBase):
    procedures: Optional[List[ProcedureCreate]] = []


class RecipePagination(OurBase):
    total: int
    itemsPerPage: int
    page: int
    recipes: List[RecipeRead] = []
