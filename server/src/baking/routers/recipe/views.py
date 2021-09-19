from fastapi import APIRouter, Depends, HTTPException
from fastapi.logger import logger


from sqlalchemy.orm import Session


from baking.models import OurBase
from baking.database.core import get_db
from baking.database.services import common_parameters, search_filter_sort_paginate

from baking.routers.recipe.models import ItemCreate, ItemRead
from baking.routers.recipe.service import create, get

router = APIRouter()


@router.get("", response_model=OurBase)
def get_items(*, common: dict = Depends(common_parameters)):
    """
    Get all recipes.
    """
    logger.info(f" this is the admin mail ")

    return search_filter_sort_paginate(model="Item", **common)


@router.get("/{recipe_id}", response_model=ItemRead)
def get_item(*, db_session: Session = Depends(get_db), item_id: int):
    """
    Update a recipe.
    """
    item = get(db_session=db_session, item_id=item_id)
    if not item:
        raise HTTPException(
            status_code=404, detail="The items with this id does not exist."
        )
    return item


@router.post("", response_model=ItemRead)
def create_item(*, db_session: Session = Depends(get_db), item_in: ItemCreate):
    """
    Create a new recipes.
    """
    item = create(db_session=db_session, item_in=item_in)
    return item
