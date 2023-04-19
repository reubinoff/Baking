from typing import List, Optional
from baking.models import NameStr
from pydantic import Field

from baking.models import BakingBaseModel

from baking.routers.ingredients.models import (
    Ingredient,
    IngredientCreate,
    IngredientRead,
)


############################################################
# Pydantic models...
############################################################


class Step(BakingBaseModel):
    """
    for example: mixing, mix all the ingredients, 10 seconds
    """
    name: NameStr
    description: Optional[str] = Field(None, nullable=True, min_length=2)
    duration_in_seconds: int = Field(1, gt=0, lt=100000)


class StepUpdate(Step):
    description: Optional[str] = Field(None, nullable=True, min_length=2)
    duration_in_seconds: Optional[int] = Field(None, gt=0, lt=100000)

############################################################

class Procedure(BakingBaseModel):
    name: NameStr
    description: Optional[str] = Field(None, nullable=True, min_length=2)
    order: Optional[int] = Field(1, gt=0, lt=100)
    steps: Optional[List[Step]]
    ingredients: Optional[List[IngredientRead]]

    @property
    def total_liquid(self) -> int:  # TODO: need to cover if the units are different
        liquid = 0
        if self.ingredients is not None:
            i: Ingredient = None
            for i in self.ingredients:
                if i.is_liquid is True:
                    liquid = liquid + i.quantity

        return liquid

    @property
    def total_solid(self) -> int:
        solid = 0
        if self.ingredients is not None:
            i: Ingredient = None
            for i in self.ingredients:
                if i.is_liquid is False:
                    solid = solid + i.quantity

        return solid
    
    @property
    def procedure_hydration(self) -> int:
        if self.total_solid > 0:
            return int((self.total_liquid / self.total_solid) * 100)
        return 100  # precent hydration

    @property
    def duration_in_seconds(self) -> int:
        total_time = 0
        if self.steps is not None:
            s: Step = None
            for s in self.steps:
                total_time = total_time + s.duration_in_seconds
        else:
            pass
            print("no steps")
        return total_time
############################################################
# Pydantic models...
############################################################


class ProcedureRead(Procedure):
    pass


class ProcedureCreate(Procedure):
    ingredients: Optional[List[IngredientCreate]] = []
    steps: Optional[List[Step]] = []


class ProcedureUpdate(Procedure):
    name: Optional[NameStr]
    ingredients: Optional[List[IngredientCreate]] = []
    steps: Optional[List[StepUpdate]] = []
