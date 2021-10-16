def test_get(session, recipe):
    from baking.routers.recipe.service import get

    t_recipe = get(db_session=session, recipe_id=recipe.id)
    assert t_recipe.id == recipe.id
