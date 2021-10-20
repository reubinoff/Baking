def test_create_and_update(session, procedures, procedure):
    from baking.routers.recipe.service import create, update
    from baking.routers.recipe.models import RecipeCreate, RecipeUpdate, Recipe

    recipe_name = "test"

    recipe_in = RecipeCreate(name=recipe_name, procedures=procedures)

    recipe = create(db_session=session, recipe_in=recipe_in)
    assert recipe
    assert len(recipe.procedures) == len(procedures)
    assert recipe.procedures[0].recipe.name == recipe_name

    new_procedures = recipe.procedures + [procedure]
    updated_recipe = RecipeUpdate(procedures=new_procedures)
    print(recipe.dict())
    recipe = update(db_session=session, recipe=recipe, recipe_in=updated_recipe)
    assert recipe
    assert len(recipe.procedures) == len(procedures) + 1
