import pytest
from baking.routers.recipe.service import get, delete, get_all, create, update
from baking.exceptions import InvalidFilterError
from baking.database.services import search_filter_sort_paginate, CommonQueryParams
from baking.models import FilterCriteria, FilterOperator
from baking.routers.recipe.models import RecipeCreate, RecipeUpdate


COLLECTION_RECIPE = "recipes"

@pytest.mark.asyncio
async def test_get(database, recipe_factory):
    recipe = await recipe_factory.create_async()
    t_recipe = await get(db=database, recipe_id=recipe.id)
    assert t_recipe.id == recipe.id
    assert isinstance(t_recipe.cdn_url, str) 


@pytest.mark.asyncio
async def test_search_filter_not_list(database, recipe_factory):
    recipe = await recipe_factory.create_async()
    name = recipe.name

    filter_critiria = FilterCriteria(
        name="name", operator=FilterOperator.EQUALS, value=f"{name}")
    query = CommonQueryParams(filter_criteria=filter_critiria)
    with pytest.raises(InvalidFilterError) as exc_info:
        _ = await search_filter_sort_paginate(db=database, collection_name=COLLECTION_RECIPE, params=query)
    assert 'Invalid filter: filter is not a list' == exc_info.value.message


@pytest.mark.asyncio
async def test_search_filter_sort_paginate_query_equal(database, recipe_factory):
    recipe = await recipe_factory.create_async()
    name = recipe.name

    filter_critiria = FilterCriteria(name="name", operator=FilterOperator.EQUALS, value=f"{name}")
    query = CommonQueryParams(filter_criteria=[filter_critiria])

    results = await search_filter_sort_paginate(db=database, collection_name=COLLECTION_RECIPE, params=query)
    
    assert results
    assert results["items"]
    assert len(results["items"]) > 0
    assert results["items"][0]['name'] == name


@pytest.mark.asyncio
async def test_search_filter_sort_paginate_query_contains(database, recipe_factory):
    total = 4
    _ = await recipe_factory.create_batch_async(total)


    filter_critiria = FilterCriteria(
        name="name", operator=FilterOperator.CONTAINS, value="recipe")
    query = CommonQueryParams(filter_criteria=[filter_critiria])

    results = await search_filter_sort_paginate(db=database, collection_name=COLLECTION_RECIPE, params=query)

    assert results
    assert results["items"]
    assert len(results["items"]) == total


@pytest.mark.asyncio
async def test_search_filter_sort_paginate_query_contains_paging(database, recipe_factory):
    total = 4
    _ = await recipe_factory.create_batch_async(total)
    
    

    filter_critiria = FilterCriteria(
        name="name", operator=FilterOperator.CONTAINS, value="recipe")
    query = CommonQueryParams(filter_criteria=[filter_critiria], page=1, items_per_page=2)

    results = await search_filter_sort_paginate(db=database, collection_name=COLLECTION_RECIPE, params=query )

    assert results
    assert results["items"]
    assert len(results["items"]) == 2
    query = CommonQueryParams(
        filter_criteria=[filter], page=2, items_per_page=2)

    results_2 = await search_filter_sort_paginate(db=database, collection_name=COLLECTION_RECIPE, params=query)
    assert results_2
    assert results_2["items"]
    assert len(results_2["items"]) == 2

    assert results["items"][0]['name'] != results_2["items"][0]['name']
    query = CommonQueryParams(
        filter_criteria=[filter], page=2, items_per_page=1)

    results_3 = await search_filter_sort_paginate(db=database, collection_name=COLLECTION_RECIPE, params=query)
    assert results_3
    assert results_3["items"]
    assert len(results_3["items"]) == 1
    assert results["items"][1]['name'] == results_3["items"][0]['name']


@pytest.mark.asyncio
async def test_search_filter_sort_by_name(database, recipe_factory):
    total = 4
    _ = await recipe_factory.create_batch_async(total)
    
    

    filter_critiria = FilterCriteria(
        name="name", operator=FilterOperator.CONTAINS, value="recipe")
    query = CommonQueryParams(
        filter_criteria=[filter_critiria], sort_by='name', descending=True)
    results = await search_filter_sort_paginate(db=database, collection_name=COLLECTION_RECIPE, params=query)

    assert results
    assert results["items"]
    assert len(results["items"]) == total
    assert results["items"][0]['name'] > results["items"][1]['name']
    query = CommonQueryParams(
        filter_criteria=[filter], sort_by='name', descending=False)
    results = await search_filter_sort_paginate(db=database, collection_name=COLLECTION_RECIPE, params=query)
    assert results
    assert results["items"]
    assert len(results["items"]) == total
    assert results["items"][0]['name'] < results["items"][1]['name']


@pytest.mark.asyncio
async def test_search_filter_not_found(database, recipe_factory):
    total = 4
    _ = await recipe_factory.create_batch_async(total)
    
    filter_critiria = FilterCriteria(
        name="name", operator=FilterOperator.CONTAINS, value="moshe")
    query = CommonQueryParams(
        filter_criteria=[filter_critiria], sort_by='name', descending=True)
    results = await search_filter_sort_paginate(db=database, collection_name=COLLECTION_RECIPE, params=query)

    assert results
    assert isinstance(results["items"], list)
    assert len(results["items"]) == 0


@pytest.mark.asyncio
async def test_get_all(database, recipe_factory):
    total = 10
    recipes = await recipe_factory.create_batch_async(total)

    t_recipes = await get_all(db=database)
    assert t_recipes
    assert len(t_recipes) == len(recipes)


@pytest.mark.asyncio
async def test_create(database, procedures):
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
    assert t_recipe.description == recipe.description

@pytest.mark.asyncio
async def test_delete(database, recipe_factory):
    recipe = await recipe_factory.create_async()
    recipe_id = recipe.id

    await delete(db=database, recipe_id=recipe_id)
    assert not await get(db=database, recipe_id=recipe_id)
