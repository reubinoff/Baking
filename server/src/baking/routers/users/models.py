from typing import List, Optional

from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from baking.database.core import Base
from baking.models import OurBase, TimeStampMixin


############################################################
# SQL models...
############################################################
class User(Base, TimeStampMixin):
    """ """

    id = Column(Integer, primary_key=True)
    username = Column(String(32))

    recipes = relationship("Recipe", backref="user")


############################################################
# Pydantic models...
############################################################
class UserBase(OurBase):
    username: str
    description: Optional[str]


class UserRead(UserBase):
    id: Optional[int]


class UserCreate(UserBase):
    pass


class UserPagination(OurBase):
    total: int
    users: List[UserBase] = []
