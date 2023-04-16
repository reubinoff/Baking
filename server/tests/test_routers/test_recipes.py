import pytest

COLLECTION_RECIPE = "recipes"

@pytest.mark.asyncio
async def test_get(database, recipe_factory):
    recipe = await recipe_factory.create_async()
    from baking.routers.recipe.service import get
    t_recipe = await get(db=database, recipe_id=recipe.id)
    assert t_recipe.id == recipe.id
    assert t_recipe.cdn_url 


@pytest.mark.asyncio
async def test_search_filter_not_list(database, recipe_factory):
    recipe = await recipe_factory.create_async()
    name = recipe.name
    from baking.database.services import search_filter_sort_paginate, common_parameters
    from baking.models import FilterCriteria, FilterOperator
    from baking.exceptions import InvalidFilterError

    filter = FilterCriteria(
        name="name", operator=FilterOperator.EQUALS, value=f"{name}")
    
    with pytest.raises(InvalidFilterError) as exc_info:
        results = await search_filter_sort_paginate(db=database, collection_name=COLLECTION_RECIPE, filter_criteria=filter)
    assert 'Invalid filter: filter is not a list' == exc_info.value.detail


@pytest.mark.asyncio
async def test_search_filter_sort_paginate_query_equal(database, recipe_factory):
    recipe = await recipe_factory.create_async()
    name = recipe.name
    from baking.database.services import search_filter_sort_paginate, common_parameters
    from baking.models import FilterCriteria, FilterOperator

    filter = FilterCriteria(name="name", operator=FilterOperator.EQUALS, value=f"{name}")
    results = await search_filter_sort_paginate(db=database, collection_name=COLLECTION_RECIPE, filter_criteria=[filter])
    
    assert results
    assert results["items"]
    assert len(results["items"]) > 0
    assert results["items"][0]['name'] == name


@pytest.mark.asyncio
async def test_search_filter_sort_paginate_query_contains(database, recipe_factory):
    TOTAL = 4
    recipe = await recipe_factory.create_batch_async(TOTAL)
    from baking.database.services import search_filter_sort_paginate, common_parameters
    from baking.models import FilterCriteria, FilterOperator

    filter = FilterCriteria(
        name="name", operator=FilterOperator.CONTAINS, value=f"recipe")
    results = await search_filter_sort_paginate(db=database, collection_name=COLLECTION_RECIPE, filter_criteria=[filter])

    assert results
    assert results["items"]
    assert len(results["items"]) == TOTAL


@pytest.mark.asyncio
async def test_search_filter_sort_paginate_query_contains_paging(database, recipe_factory):
    TOTAL = 4
    _ = await recipe_factory.create_batch_async(TOTAL)
    from baking.database.services import search_filter_sort_paginate, common_parameters
    from baking.models import FilterCriteria, FilterOperator

    filter = FilterCriteria(
        name="name", operator=FilterOperator.CONTAINS, value=f"recipe")
    results = await search_filter_sort_paginate(db=database, collection_name=COLLECTION_RECIPE, filter_criteria=[filter], page=1, items_per_page=2)

    assert results
    assert results["items"]
    assert len(results["items"]) == 2

    results_2 = await search_filter_sort_paginate(db=database, collection_name=COLLECTION_RECIPE, filter_criteria=[filter], page=2, items_per_page=2)
    assert results_2
    assert results_2["items"]
    assert len(results_2["items"]) == 2

    assert results["items"][0]['name'] != results_2["items"][0]['name']

    results_3 = await search_filter_sort_paginate(db=database, collection_name=COLLECTION_RECIPE, filter_criteria=[filter], page=2, items_per_page=1)
    assert results_3
    assert results_3["items"]
    assert len(results_3["items"]) == 1
    assert results["items"][1]['name'] == results_3["items"][0]['name']


@pytest.mark.asyncio
async def test_search_filter_sort_by_name(database, recipe_factory):
    TOTAL = 4
    _ = await recipe_factory.create_batch_async(TOTAL)
    from baking.database.services import search_filter_sort_paginate, common_parameters
    from baking.models import FilterCriteria, FilterOperator

    filter = FilterCriteria(
        name="name", operator=FilterOperator.CONTAINS, value=f"recipe")
    results = await search_filter_sort_paginate(db=database, collection_name=COLLECTION_RECIPE, filter_criteria=[filter], sort_by='name', descending=True)

    assert results
    assert results["items"]
    assert len(results["items"]) == TOTAL
    assert results["items"][0]['name'] > results["items"][1]['name']

    results = await search_filter_sort_paginate(db=database, collection_name=COLLECTION_RECIPE, filter_criteria=[filter], sort_by='name', descending=False)
    assert results
    assert results["items"]
    assert len(results["items"]) == TOTAL
    assert results["items"][0]['name'] < results["items"][1]['name']
    

@pytest.mark.asyncio
async def test_get_all(database, recipe_factory):
    TOTAL = 10
    recipes = await recipe_factory.create_batch_async(TOTAL)
    from baking.routers.recipe.service import get_all

    t_recipes = await get_all(db=database)
    assert t_recipes
    assert len(t_recipes) == len(recipes)


@pytest.mark.asyncio
async def test_create(database, procedures):
    from baking.routers.recipe.service import create
    from baking.routers.recipe.models import RecipeCreate
    from baking.routers.recipe.service import get

    recipe_name = "test"

    recipe_in = RecipeCreate(name=recipe_name, procedures=procedures)

    recipe = await create(db=database, recipe_in=recipe_in)
    assert recipe
    assert len(recipe.procedures) == len(procedures)
    assert recipe.name == recipe_name
    
    t_recipe = await get(db=database, recipe_id=recipe.id)
    assert t_recipe
    assert len(t_recipe.procedures) == len(procedures)
    assert t_recipe.name == recipe_name
    assert t_recipe.id == recipe.id


@pytest.mark.asyncio
async def test_update(database, recipe_factory):
    recipe = await recipe_factory.create_async()
    from baking.routers.recipe.service import update
    from baking.routers.recipe.models import RecipeUpdate

    name = "Updated name"
    recipe.name = name
    recipe_in = RecipeUpdate(
        name=name,
    )
    t_recipe = await update(
        db=database,
        recipe_id=recipe.id,
        recipe_in=recipe_in,
    )
    assert t_recipe.name == name

@pytest.mark.asyncio
async def test_delete(database, recipe_factory):
    recipe = await recipe_factory.create_async()
    recipe_id = recipe.id
    from baking.routers.recipe.service import get, delete

    await delete(db=database, recipe_id=recipe_id)
    assert not await get(db=database, recipe_id=recipe_id)
