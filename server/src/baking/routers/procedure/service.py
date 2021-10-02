from typing import Optional, List

from .models import RecipeRead, ItemCreate, Recipe


def get(*, db_session, item_id: int) -> Optional[Recipe]:
    """Returns a item based on the given item id."""
    return db_session.query(Recipe).filter(Recipe.id == item_id).one_or_none()


def get_all(*, db_session) -> List[Optional[Recipe]]:
    """Returns all items."""
    return db_session.query(Recipe)


def create(*, db_session, item_in: ItemCreate) -> Recipe:
    """Creates a new item."""
    item = Recipe(**item_in.dict())

    db_session.add(item)
    db_session.commit()
    return item
