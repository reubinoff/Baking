import logging
from typing import Annotated, Any
from baking.utils.azure_storage import delete_image_from_blob, upload_image_to_blob
from baking.utils.general import is_image
from motor.motor_asyncio import AsyncIOMotorDatabase

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi import status


from baking.models import PrimaryKey, PyObjectId
from baking.database.manage import get_db
from baking.database.services import  search_filter_sort_paginate, CommonQueryParams

from baking.routers.recipe.models import (
    RecipeCreate,
    RecipePagination,
    RecipeRead,
    RecipeUpdate,
)
from baking.routers.recipe.service import create, get, delete, update, update_image

LOGGER = logging.getLogger(__name__)

appDb = Annotated[AsyncIOMotorDatabase, Depends(get_db)]

router = APIRouter()


@router.get("", response_model=RecipePagination)
async def get_recipes(*, db: appDb, common: Annotated[CommonQueryParams, Depends()]):
    """
    Get all recipes.
    """
    LOGGER.info("Get Recipes filter={0}".format(common.filter_criteria))
    pagination = await search_filter_sort_paginate(
        collection_name="recipe", params=common)
    return RecipePagination(**pagination).dict()


@router.get("/{recipe_id}", response_model=RecipeRead)
async def get_recipe(*, db: appDb, recipe_id: PrimaryKey):
    """
    Get a recipe.
    """
    try:
        recipe = await check_and_raise(db=db, recipe_id=recipe_id)
        return recipe
    except HTTPException as e:
        raise e
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("")
async def create_recipe(*, db: appDb, recipe_in: RecipeCreate):
    """
    Create a new recipes.
    """
    try:
        recipe = await create(db=db, recipe_in=recipe_in)
        return recipe
    except HTTPException as e:
        raise e
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="failed to create recipe",
        )


@router.delete("/{recipe_id}", response_model=RecipeRead)
async def delete_recipe(*, db: appDb, recipe_id: PrimaryKey):
    """Delete a recipe."""
    try:
        recipe = await check_and_raise(db=db, recipe_id=recipe_id)
        image_to_delete = recipe.image
        await delete(db=db, recipe_id=recipe_id)
        delete_image_from_blob(image_to_delete)
        return recipe
    except HTTPException as e:
        raise e
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete recipe",
        )


@router.put("/{recipe_id}", response_model=RecipeRead)
async def update_recipe(
    *,
    db: appDb,
    recipe_id: PrimaryKey,
    recipe_in: RecipeUpdate
):
    """Update a recipe."""
    try:
        recipe = await check_and_raise(db=db, recipe_id=recipe_id)
        recipe = await update(db=db, recipe_id=recipe_id, recipe_in=recipe_in)
        return recipe
    except HTTPException as e:
        raise e
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update recipe",
        )


async def check_and_raise(db, recipe_id: str) -> RecipeRead:
    _id = recipe_id
    try:
        _id = PyObjectId(_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid recipe id",
        )
    recipe = await get(db=db, recipe_id=_id)
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The recipe with this id does not exist",
        )
    return recipe

@router.post("/{recipe_id}/img")
async def update_recipe_img(*,
                            db: appDb,
                            recipe_id: PrimaryKey,
                            file: UploadFile = File(...)):
    """Update a recipe image."""
    if file is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file was uploaded.",
        )
    try:
        recipe = check_and_raise(db=db, recipe_id=recipe_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        LOGGER.exception(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update recipe img",
        )
    is_file_image = is_image(file.content_type)

    try:
        uploaded_file = upload_image_to_blob(file.filename, file.file.read())
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Upload failed",
        )
    try:
        recipe = update_image(db=db,
                              recipe=recipe, image=uploaded_file)
    except Exception as e:
        delete_image_from_blob(uploaded_file.identifier)
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Update failed",
        )
    return {"file_path": file.filename, "is_valid": is_file_image, **uploaded_file.dict()}
