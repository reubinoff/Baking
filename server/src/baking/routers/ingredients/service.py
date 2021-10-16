from typing import Optional, List

from .models import IngredientRead, IngredientCreate, Ingredient


def get(*, db_session, ingredient_id: int) -> Optional[Ingredient]:
    """Returns a ingredient based on the given ingredient id."""
    return (
        db_session.query(Ingredient)
        .filter(Ingredient.id == ingredient_id)
        .one_or_none()
    )


def get_all(*, db_session) -> List[Optional[Ingredient]]:
    """Returns all ingredients."""
    return db_session.query(Ingredient)


def create(*, db_session, ingredient_in: IngredientCreate) -> Ingredient:
    """Creates a new ingredient."""
    ingredient = Ingredient(**ingredient_in.dict())

    db_session.add(ingredient)
    db_session.commit()
    return ingredient
