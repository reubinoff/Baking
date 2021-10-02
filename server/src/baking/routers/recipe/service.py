from typing import Optional, List

from .models import RecipeRead, Recipe, RecipeCreate


def get(*, db_session, item_id: int) -> Optional[Recipe]:
    """Returns a recipe based on the given item id."""
    return db_session.query(Recipe).filter(Recipe.id == item_id).one_or_none()


def get_all(*, db_session) -> List[Optional[Recipe]]:
    """Returns all items."""
    return db_session.query(Recipe)


def create(*, db_session, recipe_in: RecipeCreate) -> Recipe:
    """Creates a new item."""
    recipe = Recipe(**recipe_in.dict())

    db_session.add(recipe)
    db_session.commit()
    return recipe
