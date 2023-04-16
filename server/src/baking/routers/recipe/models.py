from datetime import datetime
from typing import List, Optional
# from baking.routers.steps.models import Step
from pydantic import Field
import random

# from baking.models import OurBase, PrimaryKey, TimeStampMixin, NameStr
from baking.config import settings
from baking.models import BakingBaseModel, NameStr, PyObjectId

from baking.routers.procedure.models import ProcedureCreate, ProcedureRead
from baking.routers.ingredients.models import IngredientRead

# from baking.routers.users.models import User, UserRead


############################################################
# Pydantic models...
############################################################

class RecipeImage(BakingBaseModel):
    imageurl: str
    identidier: str

class Recipe(BakingBaseModel):
    name: NameStr
    description: Optional[str] = Field(None, nullable=True)


class RecipeRead(Recipe):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    hydration: int
    created_at: datetime
    updated_at: datetime

    cdn_url: Optional[str]
    total_recipe_time: Optional[int]

    image: Optional[RecipeImage]




    procedures: List[ProcedureRead]

    @property    
    def cdn_url(self) -> str:
        if not self.image or not self.image.identidier:
            image_id = 200 + random.randint(1, 30)
            return f"https://baconmockup.com/300/{ image_id }"
        return f"{settings.azure_cdn_storage_base_url}/{self.image.identidier}"

    @property
    def hydration(self) -> int:
        if self.total_solid > 0:
            return int((self.total_liquid / self.total_solid) * 100)
        return 100  # precent hydration

    @property
    def total_recipe_time(self) -> int:
        return sum(p.duration_in_seconds for p in self.procedures or [])

    @property 
    def total_liquid(self) -> int:
        return sum(p.total_liquid for p in self.procedures or [])
    @property  
    def total_solid(self) -> int:
        return sum(p.total_solid for p in self.procedures or [])

    @property
    def ingredients(self) -> List[IngredientRead]:
        max_precentage_liquid: float = self.hydration/100
        # Use a defaultdict to simplify the logic of adding ingredients to the dictionary
        ingredients = dict()
        for p in self.procedures:
            for i in p.ingredients or []:
                if i.name not in ingredients:
                    ingredients[i.name] = IngredientRead(**i.dict())
                else:
                    ingredients[i.name].quantity += i.quantity
                #TODO normilzed units

                # Compute percentage based on whether ingredient is liquid or solid
                if i.is_liquid:
                    ingredients[i.name].precentage = round(
                        (ingredients[i.name].quantity / self.total_liquid) * max_precentage_liquid, 2)
                else:
                    ingredients[i.name].precentage = round(
                        (ingredients[i.name].quantity / self.total_solid), 2)

        return list(ingredients.values())

class RecipeCreate(Recipe):
    procedures: Optional[List[ProcedureCreate]] = []


class RecipeUpdate(Recipe):
    name: Optional[NameStr] = None
    procedures: Optional[List[ProcedureCreate]] = []

