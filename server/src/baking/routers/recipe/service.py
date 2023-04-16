from typing import Optional, List
from datetime import datetime
from bson.objectid import ObjectId
from baking.models import FileUploadData

from baking.routers.recipe.models import RecipeRead, RecipeCreate, RecipeUpdate

from baking.routers.procedure.service import get_or_create as get_or_create_procedure
from baking.routers.ingredients.models import IngredientRead

RECIPE_COLLECTION_NAME = "recipes"
def get_collection(db):
    return db[RECIPE_COLLECTION_NAME]


async def get(*, db, recipe_id: int) -> Optional[RecipeRead]:
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


async def create(*, db, recipe_in: RecipeCreate) -> Optional[RecipeRead]:
    """Creates a new Recipe."""
    collection = get_collection(db)
    recipe_in.created_at = recipe_in.updated_at = datetime.now()
    recipe = recipe_in.dict()
    created_recipe = await collection.insert_one(recipe)
    return RecipeRead(**recipe)


async def update(*, db, recipe_in: RecipeUpdate) -> Optional[RecipeRead]:
    """Updates a recipe."""
    collection = get_collection(db)
    recipe_id = recipe_in.id
    recipe_in.updated_at = datetime.now()
    recipe_oid = ObjectId(recipe_id)
    update_query = {"$set": recipe_in.dict(exclude_unset=True)}
    result = await collection.update_one({"_id": recipe_oid}, update_query, upsert=True)
    if not result.matched_count or not result.modified_count:
        return None
    recipe = await collection.find_one({"_id": recipe_oid})
    return RecipeRead(**recipe)


async def update_image(*, db, recipe_id: int, image: FileUploadData) -> Optional[RecipeRead]:
    """Updates the image of a recipe."""
    img_dict = {"image": image.dict()}
    return await update(db=db, recipe_in=RecipeUpdate(id=recipe_id, **img_dict))


async def delete(*, db, recipe_id: int) -> bool:
    """Deletes a recipe."""
    collection = get_collection(db)
    result = await collection.delete_one({"_id": recipe_id})

    return result.deleted_count == 1


if __name__ == "__main__":
   pass