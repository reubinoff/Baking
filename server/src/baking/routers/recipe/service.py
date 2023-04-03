from typing import Optional, List
from bson.objectid import ObjectId
from baking.models import FileUploadData
from baking.routers.ingredients.enums import is_liquid

from baking.routers.recipe.models import RecipeRead, RecipeCreate, RecipeUpdate

from baking.routers.procedure.service import get_or_create as get_or_create_procedure
from baking.routers.ingredients.models import IngredientRead

RECIPE_COLLECTION_NAME = "recipes"
def get_collection(db):
    return db[RECIPE_COLLECTION_NAME]


async def get(*, db, recipe_id: int) -> Optional[RecipeRead]:
    """Returns a recipe based on the given recipe id."""
    collection = get_collection(db)
    recipe = await collection.find_one({"id": recipe_id})
    if recipe:
        return RecipeRead(**recipe)
    return None


# def _get_ingridients(*, recipe: Recipe) -> List[Optional[IngredientRead]]:
#     """Returns a ingridients list"""
#     total_liquid = 0
#     total_solid = 0
#     max_precentage_liquid: float = recipe.hydration/100
#     ingredients = dict()
#     if recipe.procedures is not None:
#         for p in recipe.procedures:
#             for i in p.ingredients:
#                 if i.name in ingredients:
#                     ingredients[i.name].quantity = ingredients[i.name].quantity + i.quantity
#                 else:
#                     ingredients[i.name] = IngredientRead(**i.dict(), is_liquid=i.is_liquid)
#                 if is_liquid(i.type):
#                     total_liquid += i.quantity ## TODO: need to cover if the units are different
#                 else:
#                     total_solid += i.quantity

#     for name, ingredient in ingredients.items():
#         if is_liquid(ingredient.type):
#             ingredient.precentage = round(
#                 (ingredient.quantity / total_liquid) * max_precentage_liquid, 2)
#         else:
#             ingredient.precentage = round(
#                 (ingredient.quantity / total_solid) , 2)

#     return list(ingredients.values())

async def get_all(*, db) -> List[Optional[RecipeRead]]:
    """Returns all recipes."""
    collection = get_collection(db)
    recipes = []
    async for recipe in collection.find():
        recipes.append(recipe)
    return recipes


def create(*, db, recipe_in: RecipeCreate):
    """Creates a new Recipe."""
    if db is None:
        return None
    collection = get_collection(db)

    recipe = recipe_in
    
    created_recipe = collection.insert_one(recipe.dict())
    return RecipeRead(**created_recipe)



def update(*, db, recipe_in: RecipeUpdate):
    """Updates a recipe."""
    collection = get_collection(db)

    # Get the ID of the recipe to update
    recipe_id = recipe_in.id

    # Convert the ID to a BSON ObjectID
    recipe_oid = ObjectId(recipe_id)

    # Build the MongoDB update query
    update_query = {}
    for key, value in recipe_in.dict(exclude_unset=True).items():
        update_query[f"$set.{key}"] = value

    # Update the recipe in the database
    result = collection.update_one({"_id": recipe_oid}, update_query)

    # Check that the update was successful
    if not result.matched_count:
       return None
    elif not result.modified_count:
       return None
    #return the updated recipe
    recipe = collection.find_one({"_id": recipe_oid})
    return RecipeRead(**recipe)



def update_image(*, db, recipe_id: int, image: FileUploadData):
    """Updates a recipe."""
    collection = get_collection(db)
    return update(db=db, recipe_in=RecipeUpdate(id=recipe_id, **image.dict()))

def delete(*, db, recipe_id: int) -> bool:
    """Deletes a recipe."""
    collection = get_collection(db)
    result = collection.delete_one({"id": recipe_id})
    return result.deleted_count == 1


if __name__ == "__main__":
   pass