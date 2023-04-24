from typing import List, Optional
from datetime import datetime
from baking.models import NameStr, BakingBaseModel
from pydantic import Field
from .enums import IngrediantUnits, IngrediantType, is_type_liquid

############################################################
# SQL models...
############################################################


class Ingredient(BakingBaseModel):
    """
    for example: water, 30, grams, flour
    """

    name: NameStr
    quantity: Optional[int] = Field(1, gt=0, lt=100000)
    units: Optional[IngrediantUnits] = Field(IngrediantUnits.grams)
    type: Optional[IngrediantType] = Field(IngrediantType.Other)

    @property
    def is_liquid(self) -> bool:
        a = is_type_liquid(self.type)
        return a


class IngredientCreate(Ingredient):
    name: NameStr
    quantity: int = Field(1, gt=0, lt=100000)
    units: IngrediantUnits = Field(IngrediantUnits.grams)
    type: IngrediantType = Field(IngrediantType.Other)


class IngredientUpdate(Ingredient):
    name: Optional[NameStr]
    quantity: Optional[int]
    units: Optional[IngrediantUnits]
    type: Optional[IngrediantType]


class IngredientRead(Ingredient):
    precentage: Optional[float] = 0.0

############################################################
