from fastapi import APIRouter, Depends, HTTPException, status


from sqlalchemy.orm import Session


from baking.models import OurBase, PrimaryKey
from baking.database.core import get_db
from baking.database.services import common_parameters, search_filter_sort_paginate

from baking.routers.ingredients.models import (
    IngredientRead,
    IngredientPagination,
    IngredientCreate,
    IngredientUpdate,
)
from baking.routers.ingredients.service import create, get, delete, update

router = APIRouter()


@router.get("", response_model=IngredientPagination)
def get_items(*, common: dict = Depends(common_parameters)):
    """
    Get all ingredients.
    """
    return search_filter_sort_paginate(model="Ingredient", **common)


@router.get("/{ingredient_id}", response_model=IngredientRead)
def get_ingredient(*, db_session: Session = Depends(get_db), ingredient_id: int):
    """
    Update a ingredient.
    """
    ingredient = get(db_session=db_session, ingredient_id=ingredient_id)
    if not ingredient:
        raise HTTPException(
            status_code=404, detail="The ingredient with this id does not exist."
        )
    return ingredient


@router.post("", response_model=IngredientRead)
def create_ingredient(
    *, db_session: Session = Depends(get_db), ingredient_in: IngredientCreate
):
    """
    Create a new ingredient.
    """
    ingredient = create(db_session=db_session, ingredient_in=ingredient_in)
    return ingredient


@router.delete("/{ingredient_id}", response_model=IngredientRead)
def delete_ingredient(
    *, db_session: Session = Depends(get_db), ingredient_id: PrimaryKey
):
    """Delete a ingredient."""
    ingredient = get(db_session=db_session, ingredient_id=ingredient_id)
    if ingredient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "The ingredient with this id does not exist."}],
        )
    delete(db_session=db_session, ingredient_id=ingredient_id)
    return ingredient


@router.put("/{ingredient_id}", response_model=IngredientRead)
def update_ingredient(
    *,
    db_session: Session = Depends(get_db),
    ingredient_id: PrimaryKey,
    ingredient_in: IngredientUpdate
):
    """Update a ingredient."""
    ingredient = get(db_session=db_session, ingredient_id=ingredient_id)
    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "The ingredient with this id does not exist."}],
        )
    ingredient = update(
        db_session=db_session, ingredient=ingredient, ingredient_in=ingredient_in
    )
    return ingredient
