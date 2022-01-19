
def test_get(session, cleaner, ingredient):
    from baking.routers.ingredients.service import get

    t_ingredient = get(db_session=session, ingredient_id=ingredient.id)
    import time

    assert t_ingredient.id == ingredient.id


def test_get_all(session, ingredients):
    from baking.routers.ingredients.service import get_all

    t_ingredients = get_all(db_session=session).all()
    assert t_ingredients


def test_create(session, ingredient):
    from baking.routers.ingredients.service import create
    from baking.routers.ingredients.models import IngredientCreate
    from baking.routers.ingredients.enums import IngrediantType, IngrediantUnits

    data = {
        "name": "ingredient_name",
        "quantity": 239,
        "units": IngrediantUnits.grams,
        "type": IngrediantType.flour,
    }

    ingredient_in = IngredientCreate(**data)
    # print(recipe_in.dict())
    ingredient = create(db_session=session, ingredient_in=ingredient_in)
    assert ingredient


def test_update(session, ingredient):
    from baking.routers.ingredients.service import update
    from baking.routers.ingredients.models import IngredientUpdate

    name = "Updated name"

    ingredient_in = IngredientUpdate(
        name=name,
    )
    recipe = update(
        db_session=session,
        ingredient=ingredient,
        ingredient_in=ingredient_in,
    )
    assert ingredient.name == name


def test_delete(session, ingredient):
    from baking.routers.ingredients.service import get, delete

    delete(db_session=session, ingredient_id=ingredient.id)
    assert not get(db_session=session, ingredient_id=ingredient.id)
