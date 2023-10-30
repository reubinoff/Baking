from datetime import datetime
from typing import List, Optional, Annotated

from pydantic import Field

from pydantic import BaseModel, field_serializer, computed_field, AliasChoices
from baking.config import settings
from baking.models import BakingBaseModel, NameStr, PyObjectId, ObjectId

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
    description: Optional[str] = Field(None)
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @field_serializer('created_at', 'updated_at')
    def serialize_created_at(self, dt: datetime, _info):
        return dt.isoformat(timespec='seconds')



class RecipeRead(Recipe):
    # id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    id: PyObjectId = Field(
        alias="_id", validation_alias=AliasChoices("id", "_id"))

    image: Optional[RecipeImage] = None

    procedures: List[ProcedureRead]


    @field_serializer('id')
    def serialize_updated_at(self, _id: PyObjectId, _info):
        return str(_id)

    # propeties #######################
    @computed_field
    def cdn_url(self) -> str:
        if not self.image or not self.image.identifier:
            image_id = 200 + int(str(self.id)[:1])
            return f"https://baconmockup.com/300/{ image_id }"
        i = self.image.identifier
        return f"{settings.azure_cdn_storage_base_url}/{i}"

    @computed_field
    def hydration(self) -> int:
        if self.total_solid > 0:
            return int((self.total_liquid / self.total_solid) * 100)
        return 100  # precent hydration

    @computed_field(return_type=int)
    def total_recipe_time(self) -> int:
        return sum(p.duration_in_seconds for p in self.procedures or [])

    @computed_field
    def total_liquid(self) -> int:
        return sum(p.total_liquid for p in self.procedures or [])
    
    @computed_field
    def total_solid(self) -> int:
        return sum(p.total_solid for p in self.procedures or [])

    @computed_field
    def ingredients(self) -> List[IngredientRead]:
        max_precentage_liquid: float = self.hydration/100
        # Use a defaultdict to simplify the logic of adding ingredients to the dictionary
        ingredients = dict()
        for p in self.procedures:
            for i in p.ingredients or []:
                if i.name not in ingredients:
                    ingredients[i.name] = IngredientRead(**i.model_dump())
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
    procedures: Optional[List[ProcedureCreate]]


class RecipeUpdate(Recipe):
    name: Optional[NameStr] = Field(None)
    procedures: Optional[List[ProcedureUpdate]] = Field(None)
    created_at: Optional[datetime] = Field(None) 
    updated_at: datetime = Field(default_factory=datetime.now)
    image: Optional[RecipeImage] = Field(None)


class RecipePagination(BaseModel):
    total: int
    itemsPerPage: int
    page: int
    items: List[RecipeRead] = []
