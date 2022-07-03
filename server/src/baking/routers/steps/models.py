from typing import Optional

from sqlalchemy import (
    Column,
    Integer,
    String,
)
from baking.database.core import Base
from baking.models import NameStr, OurBase, PrimaryKey
from baking.models import ProcedureMixin
from pydantic import Field

############################################################
# SQL models...
############################################################

MAX_DURATION = 1000000

class Step(Base, ProcedureMixin):
    """
    for example: mixing, mix all the ingredients, 10 seconds
    """

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    duration_in_seconds = Column(Integer, nullable=True)


############################################################
# Pydantic models...
############################################################
class StepBase(OurBase):
    name: NameStr
    description: Optional[str] = Field(None, nullable=True)
    duration_in_seconds: Optional[int] = Field(1, gt=0, lt=MAX_DURATION)
    

class StepRead(StepBase):
    id: PrimaryKey
    procedure_id: PrimaryKey


class StepCreate(StepBase):
    id: Optional[PrimaryKey]
    name: NameStr
    description: Optional[str] = Field(None, nullable=True)
    duration_in_seconds: Optional[int] = Field(1, gt=0, lt=MAX_DURATION)
    # procedure_id: PrimaryKey



class StepUpdate(StepBase):
    description: Optional[str] = Field(None, nullable=True)
    duration_in_seconds: Optional[int] = Field(1, gt=0, lt=MAX_DURATION)
