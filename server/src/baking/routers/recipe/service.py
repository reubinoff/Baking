from typing import Optional, List

from .models import RecipeRead, Recipe, RecipeCreate, RecipeUpdate

from baking.routers.procedure.service import create as create_procedure


def get(*, db_session, recipe_id: int) -> Optional[Recipe]:
    """Returns a recipe based on the given recipe id."""
    return db_session.query(Recipe).filter(Recipe.id == recipe_id).one_or_none()


def get_all(*, db_session) -> List[Optional[Recipe]]:
    """Returns all items."""
    return db_session.query(Recipe)


def create(*, db_session, recipe_in: RecipeCreate) -> Recipe:
    """Creates a new Recipe."""

    procedures = [
        create_procedure(db_session=db_session, procedure_in=procedure_in)
        for procedure_in in recipe_in.procedures
    ]

    recipe = Recipe(
        **recipe_in.dict(exclude={"procedures", "ingredients"}), procedures=procedures
    )

    db_session.add(recipe)
    db_session.commit()
    return recipe


def update(*, db_session, recipe: Recipe, recipe_in: RecipeUpdate) -> Recipe:
    """Updates a recipe."""
    recipe_data = recipe.dict()

    update_data = recipe_in.dict(exclude_unset=True, exclude={})

    for field in recipe_data:
        if field in update_data:
            setattr(recipe, field, update_data[field])

    db_session.commit()
    return recipe


def delete(*, db_session, recipe_id: int):
    """Deletes a recipe."""
    project = db_session.query(Recipe).filter(Recipe.id == recipe_id).first()
    db_session.delete(project)
    db_session.commit()
