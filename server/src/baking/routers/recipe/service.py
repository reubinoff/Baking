from typing import Optional, List
from datetime import datetime
from baking.models import FileUploadData, PyObjectId
from pydantic import validate_arguments, ValidationError

from motor.motor_asyncio import AsyncIOMotorCollection

from baking.routers.recipe.models import RecipeRead, RecipeCreate, RecipeUpdate


RECIPE_COLLECTION_NAME = "recipes"


def get_collection(db) -> AsyncIOMotorCollection:
    return db[RECIPE_COLLECTION_NAME]


@validate_arguments
async def get(*, db, recipe_id: PyObjectId) -> Optional[RecipeRead]:
    """Returns a recipe based on the given recipe id."""
    collection = get_collection(db)
    recipe = await collection.find_one({"_id": recipe_id})
    if recipe:
        return RecipeRead(**recipe)
    return None


async def get_all(*, db) -> List[RecipeRead]:
    """Returns all recipes."""
    collection = get_collection(db)
    recipes = []
    async for recipe in collection.find():
        recipes.append(RecipeRead(**recipe))
    return recipes


@validate_arguments
async def create(*, db, recipe_in: RecipeCreate) -> Optional[RecipeRead]:
    """Creates a new Recipe."""
    collection = get_collection(db)
    recipe_in.created_at = recipe_in.updated_at = datetime.now()
    recipe = recipe_in.dict()
    created_recipe = await collection.insert_one(recipe)
    created_recipe_item = await collection.find_one({"_id": created_recipe.inserted_id})
    return RecipeRead(**created_recipe_item)


@validate_arguments
async def update(*, db, recipe_id: PyObjectId, recipe_in: RecipeUpdate) -> Optional[RecipeRead]:
    """Updates a recipe."""
    if isinstance(recipe_id, PyObjectId) is False:
        recipe_id = PyObjectId(recipe_id)
    collection = get_collection(db)
    recipe_in.updated_at = datetime.now()
    recipe_oid = recipe_id
    update_query = {"$set": recipe_in.dict(exclude_unset=True)}
    result = await collection.update_one({"_id": recipe_oid}, update_query)
    if not result.matched_count or not result.modified_count:
        return None
    recipe = await collection.find_one({"_id": recipe_oid})
    return RecipeRead(**recipe)


@validate_arguments
async def update_image(*, db, recipe_id: PyObjectId, image: FileUploadData) -> Optional[RecipeRead]:
    """Updates the image of a recipe."""
    img_dict = {"image": image.dict()}
    return await update(db=db,recipe_id=recipe_id, recipe_in=RecipeUpdate(**img_dict))


@validate_arguments
async def delete(*, db, recipe_id: PyObjectId) -> bool:
    """Deletes a recipe."""
    collection = get_collection(db)
    result = await collection.delete_one({"_id": recipe_id})

    return result.deleted_count == 1


if __name__ == "__main__":
   pass