from baking.routers.procedure.models import Procedure
from faker import Faker
from asyncio import sleep

from typing import List, Dict

from factory.fuzzy import FuzzyChoice, FuzzyText, FuzzyDateTime, FuzzyInteger


from baking.routers.recipe.models import Recipe, RecipeRead, RecipeCreate
from baking.routers.ingredients.models import Ingredient
from baking.routers.ingredients.enums import IngrediantType, IngrediantUnits

from .mongo_db import mongo_db
from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory import AsyncPersistenceProtocol


def get_recipes_collection(db):
    return db["recipes"]


class AsyncPersistenceHandler(AsyncPersistenceProtocol[RecipeCreate]):
    async def save(self, data: RecipeCreate) -> RecipeRead:
        created_recipe = await get_recipes_collection(mongo_db).insert_one(data.dict())
        await sleep(0.0001)
        r = await get_recipes_collection(mongo_db).find_one({"_id": created_recipe.inserted_id})
        return RecipeRead(**r)

    async def save_many(self, data: List[RecipeCreate]) -> List[RecipeRead]:
        for recipe in data:
            await get_recipes_collection(mongo_db).insert_one(recipe.dict())
        await sleep(0.0001)
        return data

# class IngredientFactory(BaseFactory):
#     """Ingredient Factory."""

#     name = Sequence(lambda n: f"ingredient_{n}")
#     quantity = FuzzyInteger(1, 1000)
#     units = FuzzyChoice(list(map(str, IngrediantUnits)))
#     type = FuzzyChoice(list(map(str, IngrediantType)))

#     procedure = SubFactory(
#         'tests.factories.ProcedureFactory', ingredients=None)

#     class Meta:
#         """Factory Configuration."""

#         model = Ingredient


# class StepFactory(BaseFactory):
#     """Ingredient Factory."""

#     name = Sequence(lambda n: f"step_{n}")
#     description = Sequence(lambda n: f"step_{n}")
#     duration_in_seconds = FuzzyInteger(1, 10000)

#     procedure = SubFactory(
#         'tests.factories.ProcedureFactory', steps=None)

#     class Meta:
#         """Factory Configuration."""

#         model = Step

# class ProcedureFactory(BaseFactory):
#     """Ingredient Factory."""

#     name = Sequence(lambda n: f"procedure_{n}")
#     description = Sequence(lambda n: f"blaBla_{n}")
#     order = FuzzyInteger(1, 10)

#     ingredients = RelatedFactoryList(
#         IngredientFactory, size=3, factory_related_name="procedure")
#     steps = RelatedFactoryList(
#         StepFactory, size=3, factory_related_name="procedure")

#     class Meta:
#         """Factory Configuration."""

#         model = Procedure
        
