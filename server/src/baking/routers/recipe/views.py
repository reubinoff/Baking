import logging
from baking.utils.azure_storage import delete_image_from_blob, upload_image_to_blob
from baking.utils.general import is_image
from motor.motor_asyncio import AsyncIOMotorDatabase

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi import status


from baking.models import PrimaryKey
from baking.database.manage import get_db
from baking.database.services import common_parameters, search_filter_sort_paginate

from baking.routers.recipe.models import (
    RecipeCreate,
    RecipePagination,
    RecipeRead,
    RecipeUpdate,
)
from baking.routers.recipe.service import create, get, delete, update, update_image

LOGGER = logging.getLogger(__name__)

router = APIRouter()


@router.get("", response_model=RecipePagination)
def get_recipes(*, common: dict = Depends(common_parameters)):
    """
    Get all recipes.
    """
    LOGGER.info("Get Recipes filter={0}".format(common["filter_spec"]))
    pagination = search_filter_sort_paginate(model="Recipe", **common)
    return RecipePagination(**pagination).dict()


@router.get("/{recipe_id}", response_model=RecipeRead)
def get_recipe(*, db: AsyncIOMotorDatabase = Depends(get_db), recipe_id: int):
    """
    Get a recipe.
    """
    recipe = check_and_raise(db=db, recipe_id=recipe_id)
    return recipe


@router.post("")
def create_recipe(*, db: AsyncIOMotorDatabase = Depends(get_db), recipe_in: RecipeCreate):
    """
    Create a new recipes.
    """
    recipe = create(db=db, recipe_in=recipe_in)
    return recipe


@router.delete("/{recipe_id}", response_model=RecipeRead)
def delete_recipe(*, db: AsyncIOMotorDatabase = Depends(get_db), recipe_id: PrimaryKey):
    """Delete a recipe."""
    recipe = get(db=db, recipe_id=recipe_id)
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "The recipe with this id does not exist."}],
        )
    Identifier_to_delete = recipe.image_identidier
    delete(db=db, recipe_id=recipe_id)
    delete_image_from_blob(Identifier_to_delete)
    return recipe


@router.put("/{recipe_id}", response_model=RecipeRead)
def update_recipe(
    *,
    db: AsyncIOMotorDatabase = Depends(get_db),
    recipe_id: PrimaryKey,
    recipe_in: RecipeUpdate
):
    """Update a recipe."""
    recipe = check_and_raise(db=db, recipe_id=recipe_id)
    recipe = update(db=db, recipe=recipe, recipe_id=recipe_id, recipe_in=recipe_in)
    return recipe


def check_and_raise(db, recipe_id) -> RecipeRead:
    recipe = get(db=db, recipe_id=recipe_id)
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "The recipe with this id does not exist."}],
        )
    return recipe

@router.post("/{recipe_id}/img")
async def update_recipe_img(*,
                            db: AsyncIOMotorDatabase = Depends(get_db),
                            recipe_id: PrimaryKey,
                            file: UploadFile = File(...)):
    """Update a recipe image."""
    if file is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[{"msg": "No file was uploaded."}],
        )
    recipe = check_and_raise(db=db, recipe_id=recipe_id)
    is_file_image = is_image(file.content_type)

    try:
        uploaded_file = upload_image_to_blob(file.filename, file.file.read())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail=[{"msg": "Upload failed"}],
        )
    try:
        recipe = update_image(db=db,
                              recipe=recipe, image=uploaded_file)
    except Exception as e:
        delete_image_from_blob(uploaded_file.identidier)
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail=[{"msg": "Update failed"}],
        )
    return {"file_path": file.filename, "is_valid": is_file_image, **uploaded_file.dict()}
