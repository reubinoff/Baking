from typing import Optional, List

from .models import RecipeRead, Recipe, RecipeCreate, RecipeUpdate

from baking.routers.procedure.service import create as create_procedure
from baking.routers.procedure.service import get_or_create as get_or_create_procedure


def get(*, db_session, recipe_id: int) -> Optional[Recipe]:
    """Returns a recipe based on the given recipe id."""
    return db_session.query(Recipe).filter(Recipe.id == recipe_id).one_or_none()


def get_all(*, db_session) -> List[Optional[Recipe]]:
    """Returns all recipes."""
    return db_session.query(Recipe)


def create(*, db_session, recipe_in: RecipeCreate) -> Recipe:
    """Creates a new Recipe."""
    if db_session is None:
        return None
    procedures = []
    if recipe_in.procedures is not None and isinstance(recipe_in.procedures, List):
        procedures = [
            get_or_create_procedure(db_session=db_session, procedure_in=procedure_in)
            for procedure_in in recipe_in.procedures
        ]

    recipe = Recipe(**recipe_in.dict(exclude={"procedures"}), procedures=procedures)
    # print(recipe_in.dict())
    db_session.add(recipe)
    db_session.commit()
    return recipe


def update(*, db_session, recipe: Recipe, recipe_in: RecipeUpdate) -> Recipe:
    """Updates a recipe."""
    recipe_data = recipe.dict()

    procedures = []
    for p in recipe_in.procedures:
        print("<><><><><<>")
        procedures.append(
            get_or_create_procedure(db_session=db_session, procedure_in=p)
        )

    update_data = recipe_in.dict(exclude_unset=True, exclude={"procedures"})

    for field in recipe_data:
        if field in update_data:
            setattr(recipe, field, update_data[field])
    recipe.procedures = procedures

    db_session.commit()
    return recipe


def delete(*, db_session, recipe_id: int):
    """Deletes a recipe."""
    recipe = db_session.query(Recipe).filter(Recipe.id == recipe_id).first()
    db_session.delete(recipe)
    db_session.commit()
