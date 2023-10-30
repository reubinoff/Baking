from datetime import datetime
from asyncio import sleep

from typing import List

from baking.routers.recipe.models import RecipeRead, RecipeCreate
from baking.database.manage import init_database

from polyfactory import AsyncPersistenceProtocol


mongo_db = init_database()


def get_recipes_collection(db):
    return db["recipes"]


class AsyncPersistenceHandler(AsyncPersistenceProtocol[RecipeCreate]):
    async def save(self, data: RecipeCreate) -> RecipeRead:
        data.created_at = data.updated_at = datetime.now()
        created_recipe = await get_recipes_collection(mongo_db).insert_one(data.model_dump())
        r = await get_recipes_collection(mongo_db).find_one({"_id": created_recipe.inserted_id})
        return RecipeRead(**r)

    async def save_many(self, data: List[RecipeCreate]) -> List[RecipeRead]:
        for recipe in data:
            await get_recipes_collection(mongo_db).insert_one(recipe.model_dump())
        await sleep(0.0001)
        created_recipes = []
        async for recipe in get_recipes_collection(mongo_db).find():
            created_recipes.append(RecipeRead(**recipe))
        return created_recipes
        
