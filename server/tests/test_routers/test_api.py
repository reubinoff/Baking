import urllib
import json
import os
import pytest

from mock import patch

from baking.models import FilterCriteria, FilterOperator
from baking.routers.recipe.models import RecipeCreate, RecipeRead, RecipeUpdate

@pytest.mark.anyio
async def test_get_recipe(recipe_factory, client):
    recipe: RecipeRead = await recipe_factory.create_async()
    response = await client.get(f"/recipe/{recipe.id}")
    assert response.status_code == 200
    assert response.json() == recipe.model_dump()


@pytest.mark.anyio
async def test_get_all(recipe_factory, client):
    recipes = await recipe_factory.create_batch_async(10)
    response = await client.get("/recipe")
    assert response.status_code == 200
    # assert RecipeRead(**response.json()) == recipe
    items_data = response.json()["items"]
    assert len(items_data) == 5 # default page size is 5
    assert items_data[0] == recipes[0].model_dump()
    response = await client.get("/recipe?page=2")
    assert response.status_code == 200
    items_data = response.json()["items"]
    assert len(items_data) == 5
    assert items_data[0] == recipes[5].model_dump()
    assert isinstance(items_data[0]["cdn_url"] , str)
    
@pytest.mark.anyio
async def test_get_filter(recipe_factory, client):
    recipe = await recipe_factory.create_async()
    critiria = FilterCriteria(
        name="name", operator=FilterOperator.EQUALS, value=recipe.name)
    url_encoded_critiria = urllib.parse.quote(json.dumps([critiria.model_dump()]))
    
    response = await client.get(f"/recipe?filter={url_encoded_critiria}")
    assert response.status_code == 200
    items_data = response.json()["items"]
    assert len(items_data) == 1
    assert RecipeRead(**items_data[0]).name == recipe.name
    # take only part of the name
    critiria = FilterCriteria(
        name="name", operator=FilterOperator.CONTAINS, value=recipe.name[:3])
    url_encoded_critiria = urllib.parse.quote(json.dumps([critiria.model_dump()]))
    response = await client.get(f"/recipe?filter={url_encoded_critiria}")
    assert response.status_code == 200
    items_data = response.json()["items"]
    assert len(items_data) == 1
    assert RecipeRead(**items_data[0]).name == recipe.name

    #change the name
    critiria = FilterCriteria(
        name="name", operator=FilterOperator.EQUALS, value="REUBINOFF")
    url_encoded_critiria = urllib.parse.quote(json.dumps([critiria.model_dump()]))
    response = await client.get(f"/recipe?filter={url_encoded_critiria}")
    assert response.status_code == 200
    items_data = response.json()["items"]
    assert len(items_data) == 0


@pytest.mark.anyio
async def test_get_query(recipe_factory, client):
    recipe = await recipe_factory.create_async()
    response = await client.get(f"/recipe?q={recipe.name}")
    assert response.status_code == 200
    items_data = response.json()["items"]
    assert len(items_data) == 1
    assert RecipeRead(**items_data[0]).name == recipe.name
    # take only part of the name
    response = await client.get(f"/recipe?q={recipe.name[:3]}")
    assert response.status_code == 200
    items_data = response.json()["items"]
    assert len(items_data) == 0

    #change the name
    response = await client.get("/recipe?q=REUBINOFF")
    assert response.status_code == 200
    items_data = response.json()["items"]
    assert len(items_data) == 0


@pytest.mark.anyio
async def test_get_query_in_description(recipe_factory, client):
    recipe = await recipe_factory.create_async()
    response = await client.get(f"/recipe?q={recipe.description.split(' ')[2]}")
    assert response.status_code == 200
    items_data = response.json()["items"]
    assert len(items_data) == 1
    assert RecipeRead(**items_data[0]).name == recipe.name
    # take only part of the name
    response = await client.get(f"/recipe?q={recipe.description.split(' ')[2][:3]}")
    assert response.status_code == 200
    items_data = response.json()["items"]
    assert len(items_data) == 0



@pytest.mark.anyio
async def test_recipe_get_invalid_id(recipe_factory, client):
    _: RecipeRead = await recipe_factory.create_async()
    response = await client.get("/recipe/abc")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid recipe id"


@pytest.mark.anyio
async def test_recipe_not_found(client):
    response = await client.get("/recipe/644016caff25afc6b20de505")
    assert response.status_code == 404
    assert response.json()["detail"] == "The recipe with this id does not exist"


@pytest.mark.anyio
async def test_recipe_create(procedures, client):
    recipe = RecipeCreate(
        name="test",
        description="test",
        procedures=procedures,
    )
    response = await client.post("/recipe", json=recipe.model_dump())
    assert response.status_code == 200
    assert response.json()["name"] == recipe.name
    assert response.json()["description"] == recipe.description
    assert len(response.json()["procedures"]) == len(recipe.procedures)

    response_create = await client.get(f"/recipe/{response.json()['id']}")
    assert response_create.status_code == 200
    assert response_create.json() == response.json()


@pytest.mark.anyio
async def test_recipe_update(recipe_factory, client):
    recipe = await recipe_factory.create_async()
    recipe_update = RecipeUpdate(name="test_update")
    response = await client.put(f"/recipe/{recipe.id}", json=recipe_update.model_dump(exclude_unset=True))
    assert response.status_code == 200
    assert response.json()["name"] == recipe_update.name

    response = await client.get(f"/recipe/{recipe.id}")
    assert response.status_code == 200
    assert RecipeRead(**response.json()) == RecipeRead(**response.json())


@pytest.mark.anyio
async def test_recipe_delete(recipe_factory, client):
    recipe = await recipe_factory.create_async()
    response = await client.delete(f"/recipe/{recipe.id}")
    assert response.status_code == 200
    assert RecipeRead(**response.json()) == recipe

    response = await client.get(f"/recipe/{recipe.id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "The recipe with this id does not exist"


@pytest.mark.anyio
async def test_recipe_delete_invalid_id(recipe_factory, client):
    _: RecipeRead = await recipe_factory.create_async()
    response = await client.delete("/recipe/abc")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid recipe id"


@pytest.mark.anyio
async def test_recipe_delete_not_found(recipe_factory, client):
    _: RecipeRead = await recipe_factory.create_async()
    response = await client.delete("/recipe/644016caff25afc6b20de505")
    assert response.status_code == 404
    assert response.json()["detail"] == "The recipe with this id does not exist"


@pytest.mark.anyio
async def test_recipe_update_recipe_img(recipe_factory, client):
    recipe = await recipe_factory.create_async()
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(parent_dir + "/test_data/test.jpeg", "rb") as image_file:
        # mock the method baking.utils.azure_storage.upload_image_to_blob
        with patch("baking.utils.azure_storage.upload_image_to_blob") as mock_upload_image_to_blob:
            mock_upload_image_to_blob.return_value = 'bar'
            response = await client.post(f"/recipe/{recipe.id}/img", files={"file": image_file})
    assert response.status_code == 200
    assert response.json()["file_path"] == "test.jpeg"

    response = await client.get(f"/recipe/{recipe.id}")
    assert response.status_code == 200
    r_test = RecipeRead(**response.json())
    assert r_test.image

