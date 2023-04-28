from datetime import datetime
from typing import List, Optional

from pydantic import Field

from pydantic import BaseModel
from baking.config import settings
from baking.models import BakingBaseModel, NameStr, PyObjectId

from baking.routers.procedure.models import ProcedureCreate, ProcedureRead, ProcedureUpdate
from baking.routers.ingredients.models import IngredientRead


############################################################
# Pydantic models...
############################################################

class RecipeImage(BakingBaseModel):
    url: str
    identifier: str

class Recipe(BakingBaseModel):
    name: NameStr
    description: Optional[str] = Field(None, nullable=True)
    created_at: Optional[datetime]
    updated_at: Optional[datetime]



class RecipeRead(Recipe):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    total_recipe_time: Optional[int]

    image: Optional[RecipeImage]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    procedures: List[ProcedureRead]

    # propeties #######################

    @property
    def cdn_url(self) -> str:
        if not self.image or not self.image.identifier:
            image_id = 200 + int(str(self.id)[:1])
            return f"https://baconmockup.com/300/{ image_id }"
        i = self.image.identifier
        return f"{settings.azure_cdn_storage_base_url}/{i}"

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

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class RecipeUpdate(Recipe):
    name: Optional[NameStr]
    procedures: Optional[List[ProcedureUpdate]]
    created_at: Optional[datetime]
    updated_at: datetime = Field(default_factory=datetime.now)
    image: Optional[RecipeImage]


class RecipePagination(BaseModel):
    total: int
    itemsPerPage: int
    page: int
    items: List[RecipeRead] = []
