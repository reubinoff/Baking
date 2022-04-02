from xml.dom.minidom import Identified
from baking.utils.azure import delete_image_from_blob, upload_image_to_blob
from baking.utils.general import is_image
import filetype

from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile
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
from baking.routers.recipe.service import create, get, delete, update, update_image

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
    recipe = check_and_raise(db_session=db_session, recipe_id=recipe_id)
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
    Identifier_to_delete = recipe.image_identidier
    delete(db_session=db_session, recipe_id=recipe_id)
    delete_image_from_blob(Identifier_to_delete)
    return recipe


@router.put("/{recipe_id}", response_model=RecipeRead)
def update_recipe(
    *,
    db_session: Session = Depends(get_db),
    recipe_id: PrimaryKey,
    recipe_in: RecipeUpdate
):
    """Update a recipe."""
    check_and_raise(db_session=db_session, recipe_id=recipe_id)
    recipe = update(db_session=db_session, recipe=recipe, recipe_in=recipe_in)
    return recipe


def check_and_raise(db_session, recipe_id):
    recipe = get(db_session=db_session, recipe_id=recipe_id)
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "The recipe with this id does not exist."}],
        )
    return recipe

@router.post("/{recipe_id}/img")
async def update_recipe_img(*,
                            db_session: Session = Depends(get_db),
                            recipe_id: PrimaryKey,
                            file: UploadFile = File(...)):
    """Update a recipe image."""
    if file is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[{"msg": "No file was uploaded."}],
        )
    recipe = check_and_raise(db_session=db_session, recipe_id=recipe_id)
    is_file_image = is_image(file.content_type)

    try:
        uploaded_file = upload_image_to_blob(file.filename, file.file.read())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail=[{"msg": "Upload failed"}],
        )
    try:
        recipe = update_image(db_session=db_session,
                              recipe=recipe, image=uploaded_file)
    except Exception as e:
        delete_image_from_blob(uploaded_file.identidier)
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail=[{"msg": "Update failed"}],
        )
    return {"file_path": file.filename, "is_valid": is_file_image, **uploaded_file.dict()}
