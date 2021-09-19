from fastapi_versioning import version
from fastapi import APIRouter, Depends, HTTPException
from fastapi.logger import logger


from sqlalchemy.orm import Session


from fastapi_best_practice.models import OurBase
from fastapi_best_practice.database.core import get_db
from fastapi_best_practice.database.services import common_parameters, search_filter_sort_paginate
from fastapi_best_practice.settings.service import get_all as get_settings
from fastapi_best_practice.settings.models import Settings

from baking.routers.recipe.models import ItemCreate, ItemRead
from baking.routers.recipe.service import create, get

router = APIRouter()


@router.get("", response_model=OurBase)
@version(1)
def get_items(*, common: dict = Depends(common_parameters)):
    """
    Get all recipes.
    """
    # this the way to use the settings
    settings: Settings = get_settings(db_session=common["db_session"])
    
    logger.info(f" this is the admin mail {settings.admin_mail}")

    return search_filter_sort_paginate(model="Item", **common)


@router.get("/{item_id}", response_model=ItemRead)
@version(2)
def get_item(*, db_session: Session = Depends(get_db), item_id: int):
    """
    Update a item.
    """
    item = get(db_session=db_session, item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="The items with this id does not exist.")
    return item


@router.post("", response_model=ItemRead)
@version(1)
def create_item(*, db_session: Session = Depends(get_db), item_in: ItemCreate):
    """
    Create a new item.
    """
    item = create(db_session=db_session, item_in=item_in)
    return item
