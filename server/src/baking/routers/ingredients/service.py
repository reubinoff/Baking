from typing import Optional, List

from .models import IngredientRead, IngredientCreate, Ingredient, IngredientUpdate


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


def delete(*, db_session, ingredient_id: int):
    """Deletes a ingredient."""
    project = (
        db_session.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    )
    db_session.delete(project)
    db_session.commit()


def update(
    *, db_session, ingredient: Ingredient, ingredient_in: IngredientUpdate
) -> Ingredient:
    """Updates a ingredient."""
    ingredient_data = ingredient.dict()

    update_data = ingredient_in.dict(exclude_unset=True, exclude={})

    for field in ingredient_data:
        if field in update_data:
            setattr(ingredient, field, update_data[field])

    db_session.commit()
    return ingredient
