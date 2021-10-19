from fastapi import APIRouter, Depends, HTTPException
from fastapi.logger import logger
from fastapi import status


from sqlalchemy.orm import Session


from baking.models import OurBase, PrimaryKey
from baking.database.core import get_db
from baking.database.services import common_parameters, search_filter_sort_paginate

from baking.routers.recipe.models import (
    RecipeCreate,
    RecipePagination,
    RecipeRead,
    RecipeUpdate,
)
from baking.routers.recipe.service import create, get, delete, update

router = APIRouter()


@router.get("", response_model=RecipePagination)
def get_recipes(*, common: dict = Depends(common_parameters)):
    """
    Get all recipes.
    """
    pagination = search_filter_sort_paginate(model="Recipe", **common)
    return RecipePagination(**pagination).dict()


@router.get("/{recipe_id}", response_model=RecipeRead)
def get_recipe(*, db_session: Session = Depends(get_db), recipe_id: int):
    """
    Update a recipe.
    """
    recipe = get(db_session=db_session, recipe_id=recipe_id)
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "The recipe with this id does not exist."}],
        )
    return recipe


@router.post("", response_model=RecipeRead)
def create_recipe(*, db_session: Session = Depends(get_db), recipe_in: RecipeCreate):
    """
    Create a new recipes.
    """
    recipe = create(db_session=db_session, recipe_in=recipe_in)
    return recipe


@router.delete("/{recipe_id}", response_model=RecipeRead)
def delete_recipe(*, db_session: Session = Depends(get_db), recipe_id: PrimaryKey):
    """Delete a recipe."""
    recipe = get(db_session=db_session, recipe_id=recipe_id)
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "The recipe with this id does not exist."}],
        )
    delete(db_session=db_session, recipe_id=recipe_id)
    return recipe


@router.put("/{recipe_id}", response_model=RecipeRead)
def update_recipe(
    *,
    db_session: Session = Depends(get_db),
    recipe_id: PrimaryKey,
    recipe_in: RecipeUpdate
):
    """Update a recipe."""
    recipe = get(db_session=db_session, recipe_id=recipe_id)
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "The recipe with this id does not exist."}],
        )
    recipe = update(db_session=db_session, recipe=recipe, recipe_in=recipe_in)
    return recipe
