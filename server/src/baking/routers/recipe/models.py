from datetime import datetime
from typing import List, Optional
from pydantic import Field, validator

from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils import TSVectorType


from baking.database.core import Base
from baking.models import OurBase, PrimaryKey, TimeStampMixin, NameStr
from baking.config import settings

from baking.routers.procedure.models import Procedure, ProcedureCreate, ProcedureRead

# from baking.routers.users.models import User, UserRead


############################################################
# SQL models...
############################################################
class Recipe(Base, TimeStampMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    image_url = Column(String)
    image_identidier = Column(String)

    # auther of the recipe ###############################################################
    # public = Column(Boolean)
    # user_id = Column(Integer, ForeignKey("user.id"), index=True, nullable=False)
    ###########################################################################################

    procedures = relationship(
        "Procedure",
        order_by="asc(Procedure.order)",
        cascade="all, delete-orphan",
        back_populates="recipe",
    )

    search_vector = Column(
        TSVectorType(
            "description", "name"
        )
    )

    @hybrid_property
    def cdn_url(self):
        return f"{settings.azure_cdn_storage_base_url}/{self.image_identidier}"

    @hybrid_property
    def hydration(self) -> int:
        liquid = 0
        solid = 0
        if self.procedures is not None:
            p: Procedure = None
            for p in self.procedures:
                liquid = liquid + p.total_liquid
                solid = solid + p.total_solid
        # print(f"liquid = {liquid}")
        # print(f"solid = {solid}")
        if solid > 0:
            return int((liquid / solid) * 100)
        return 100  # precent hydration


############################################################
# Pydantic models...
############################################################
class RecipeBase(OurBase):
    name: Optional[NameStr]
    description: Optional[str] = Field(None, nullable=True)
    procedures: Optional[List[ProcedureRead]]

    @validator("name")
    def title_required(cls, v):
        if not v or "\x00" in v:
            raise ValueError("must not be empty string")
        return v


class RecipeRead(RecipeBase):
    id: PrimaryKey
    name: NameStr
    hydration: int
    # image_url: Optional[str]
    cdn_url: Optional[str]


class RecipeCreate(RecipeBase):
    name: NameStr
    procedures: Optional[List[ProcedureCreate]] = []


class RecipeUpdate(RecipeBase):
    procedures: Optional[List[ProcedureCreate]] = []


class RecipePagination(OurBase):
    total: int
    itemsPerPage: int
    page: int
    items: List[RecipeRead] = []
