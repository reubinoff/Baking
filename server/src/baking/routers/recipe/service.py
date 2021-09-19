from typing import  Optional, List

from .models import ItemRead, ItemCreate, Item



def get(*, db_session, item_id: int) -> Optional[Item]:
    """Returns a item based on the given item id."""
    return db_session.query(Item).filter(Item.id == item_id).one_or_none()


def get_all(*, db_session) -> List[Optional[Item]]:
    """Returns all items."""
    return db_session.query(Item)



def create(*, db_session, item_in: ItemCreate) -> Item:
    """Creates a new item."""
    item = Item(**item_in.dict())

    db_session.add(item)
    db_session.commit()
    return item