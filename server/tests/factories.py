from baking.routers.procedure.models import Procedure
from datetime import datetime
from asyncio import sleep

from typing import List, Dict

from baking.routers.recipe.models import Recipe, RecipeRead, RecipeCreate

from .mongo_db import mongo_db
from polyfactory import AsyncPersistenceProtocol


def get_recipes_collection(db):
    return db["recipes"]


class AsyncPersistenceHandler(AsyncPersistenceProtocol[RecipeCreate]):
    async def save(self, data: RecipeCreate) -> RecipeRead:
        data.created_at = data.updated_at = datetime.now()
        created_recipe = await get_recipes_collection(mongo_db).insert_one(data.dict())
        await sleep(0.0001)
        r = await get_recipes_collection(mongo_db).find_one({"_id": created_recipe.inserted_id})
        return RecipeRead(**r)

    async def save_many(self, data: List[RecipeCreate]) -> List[RecipeRead]:
        for recipe in data:
            await get_recipes_collection(mongo_db).insert_one(recipe.dict())
        await sleep(0.0001)
        return data
