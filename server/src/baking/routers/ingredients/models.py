from typing import List, Optional
from datetime import datetime
from baking.models import NameStr, BakingBaseModel
from pydantic import Field, computed_field
from .enums import IngredientUnits, IngredientType, is_type_liquid

############################################################
# SQL models...
############################################################


class Ingredient(BakingBaseModel):
    """
    for example: water, 30, grams, flour
    """

    name: NameStr
    quantity: Optional[int] = Field(1, gt=0, lt=100000)
    units: Optional[IngredientUnits] = Field(IngredientUnits.grams)
    type: Optional[IngredientType] = Field(IngredientType.Other)

    @computed_field
    @property
    def is_liquid(self) -> bool:
        a = is_type_liquid(self.type)
        return a


class IngredientCreate(Ingredient):
    name: NameStr
    quantity: int = Field(1, gt=0, lt=100000)
    units: IngredientUnits = Field(IngredientUnits.grams)
    type: IngredientType = Field(IngredientType.Other)


class IngredientUpdate(Ingredient):
    name: Optional[NameStr]= Field(None)
    quantity: Optional[int]= Field(None)
    units: Optional[IngredientUnits]= Field(None)
    type: Optional[IngredientType]= Field(None)


class IngredientRead(Ingredient):
    precentage: Optional[float] = 0.0

############################################################
