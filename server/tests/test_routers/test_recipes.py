def test_get(session, cleaner, recipe):
    from baking.routers.recipe.service import get

    t_recipe = get(db_session=session, recipe_id=recipe.id)
    assert t_recipe.id == recipe.id


def test_search_filter_sort_paginate_query(session, cleaner, recipe):
    name = recipe.name
    from baking.database.services import search_filter_sort_paginate, common_parameters

    results = search_filter_sort_paginate(db_session=session, model="Recipe", query_str=name)
    assert results
    assert results["items"]
    assert len(results["items"]) > 0
    assert results["items"][0].name == name


def test_search_filter_sort_paginate_filter(session, cleaner, recipe):
    name = recipe.name
    from baking.database.services import search_filter_sort_paginate, common_parameters
    filter = [{"model": "Recipe", "field": "name",
               "op": "like", "value": f"%{name}%"}]
    results = search_filter_sort_paginate(
        db_session=session, model="Recipe", filter_spec=filter)
    assert results
    assert results["items"]
    assert len(results["items"]) > 0
    assert results["items"][0].name == name


def test_get_all(session, recipes):
    from baking.routers.recipe.service import get_all

    t_recipes = get_all(db_session=session).all()
    assert t_recipes


def test_create(session, procedures):
    from baking.routers.recipe.service import create
    from baking.routers.recipe.models import RecipeCreate

    recipe_name = "test"

    recipe_in = RecipeCreate(name=recipe_name, procedures=procedures)

    recipe = create(db_session=session, recipe_in=recipe_in)
    assert recipe
    assert len(recipe.procedures) == len(procedures)
    assert recipe.procedures[0].recipe.name == recipe_name


def test_update(session, recipe):
    from baking.routers.recipe.service import update
    from baking.routers.recipe.models import RecipeUpdate

    name = "Updated name"

    recipe_in = RecipeUpdate(
        name=name,
    )
    recipe = update(
        db_session=session,
        recipe=recipe,
        recipe_in=recipe_in,
    )
    assert recipe.name == name


def test_delete(session, recipe):
    from baking.routers.recipe.service import get, delete

    delete(db_session=session, recipe_id=recipe.id)
    assert not get(db_session=session, recipe_id=recipe.id)
