from fastapi import APIRouter, Depends, HTTPException
from fastapi.logger import logger
from fastapi import status


from sqlalchemy.orm import Session


from baking.models import OurBase
from baking.database.core import get_db
from baking.database.services import common_parameters, search_filter_sort_paginate

from baking.routers.recipe.models import RecipeCreate, RecipePagination, RecipeRead
from baking.routers.recipe.service import create, get

router = APIRouter()


@router.get("", response_model=RecipePagination)
def get_recipes(*, common: dict = Depends(common_parameters)):
    """
    Get all recipes.
    """
    pagination = search_filter_sort_paginate(model="Recipe", **common)
    return RecipePagination(**pagination).dict()


# @router.get("/{recipe_id}", response_model=RecipeRead)
# def get_recipe(*, db_session: Session = Depends(get_db), recipe_id: int):
#     """
#     Update a recipe.
#     """
#     recipe = get(db_session=db_session, recipe_id=recipe_id)
#     if not recipe:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="The recipes with this id does not exist.",
#         )
#     return recipe


# @router.post("", response_model=RecipeRead)
# def create_recipe(*, db_session: Session = Depends(get_db), recipe_in: RecipeCreate):
#     """
#     Create a new recipes.
#     """
#     recipe = create(db_session=db_session, recipe_in=recipe_in)
#     return recipe
