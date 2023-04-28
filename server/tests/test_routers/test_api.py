import pytest
import urllib
import json
from mock import patch
import os
import schemathesis
from fastapi.testclient import TestClient
from schemathesis.checks import ALL_CHECKS, DEFAULT_CHECKS
from httpx import AsyncClient

from hypothesis import settings, HealthCheck

from baking.main import app
from baking.models import FilterCriteria, FilterOperator


schemathesis.fixups.install(["fast_api"])

schema = schemathesis.from_asgi("/docs/openapi.json", app, base_url="/")


@pytest.fixture(scope="session")
def token():
    client = TestClient(app)
    response = client.post(
        "/api/v1/default/auth/register",
        json={"email": "test@example.com", "password": "test123"},
    )
    assert response.status_code == 200
    return response.json()["token"]


# @schema.parametrize()
# @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
# def test_api(case):
#     # def test_api(db, token, case):
#     case.headers = case.headers or {}
#     # case.headers["Authorization"] = f"Bearer {token}"
#     response = case.call_asgi(base_url="http://testserver/")
#     case.validate_response(response, checks=DEFAULT_CHECKS)

@pytest.mark.anyio
async def test_get_recipe(recipe_factory):
    from baking.routers.recipe.models import RecipeRead

    recipe: RecipeRead = await recipe_factory.create_async()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/recipe/{recipe.id}")
    assert response.status_code == 200
    assert RecipeRead(**response.json()) == recipe


@pytest.mark.anyio
async def test_get_all(recipe_factory):
    from baking.routers.recipe.models import RecipeRead

    recipes = await recipe_factory.create_batch_async(10)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/recipe")
    assert response.status_code == 200
    # assert RecipeRead(**response.json()) == recipe
    items_data = response.json()["items"]
    assert len(items_data) == 5 # default page size is 5
    assert RecipeRead(**items_data[0]) == recipes[0]
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/recipe?page=2")
    assert response.status_code == 200
    items_data = response.json()["items"]
    assert len(items_data) == 5
    assert RecipeRead(**items_data[0]) == recipes[5]
    assert isinstance(items_data[0]["cdn_url"] , str)
    
@pytest.mark.anyio
async def test_get_filter(recipe_factory):
    from baking.routers.recipe.models import RecipeRead
    recipe = await recipe_factory.create_async()
    critiria = FilterCriteria(
        name="name", operator=FilterOperator.EQUALS, value=recipe.name)
    url_encoded_critiria = urllib.parse.quote(json.dumps([critiria.dict()]))
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/recipe?filter={url_encoded_critiria}")
    assert response.status_code == 200
    items_data = response.json()["items"]
    assert len(items_data) == 1
    assert RecipeRead(**items_data[0]).name == recipe.name
    # take only part of the name
    critiria = FilterCriteria(
        name="name", operator=FilterOperator.CONTAINS, value=recipe.name[:3])
    url_encoded_critiria = urllib.parse.quote(json.dumps([critiria.dict()]))
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/recipe?filter={url_encoded_critiria}")
    assert response.status_code == 200
    items_data = response.json()["items"]
    assert len(items_data) == 1
    assert RecipeRead(**items_data[0]).name == recipe.name

    #change the name
    critiria = FilterCriteria(
        name="name", operator=FilterOperator.EQUALS, value="REUBINOFF")
    url_encoded_critiria = urllib.parse.quote(json.dumps([critiria.dict()]))
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/recipe?filter={url_encoded_critiria}")
    assert response.status_code == 200
    items_data = response.json()["items"]
    assert len(items_data) == 0


@pytest.mark.anyio
async def test_get_query(recipe_factory):
    from baking.routers.recipe.models import RecipeRead
    recipe = await recipe_factory.create_async()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/recipe?q={recipe.name}")
    assert response.status_code == 200
    items_data = response.json()["items"]
    assert len(items_data) == 1
    assert RecipeRead(**items_data[0]).name == recipe.name
    # take only part of the name
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/recipe?q={recipe.name[:3]}")
    assert response.status_code == 200
    items_data = response.json()["items"]
    assert len(items_data) == 0

    #change the name
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/recipe?q=REUBINOFF")
    assert response.status_code == 200
    items_data = response.json()["items"]
    assert len(items_data) == 0


@pytest.mark.anyio
async def test_recipe_get_invalid_id(recipe_factory):
    from baking.routers.recipe.models import RecipeRead

    _: RecipeRead = await recipe_factory.create_async()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/recipe/abc")
        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid recipe id"


@pytest.mark.anyio
async def test_recipe_not_found():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/recipe/644016caff25afc6b20de505")
    assert response.status_code == 404
    assert response.json()["detail"] == "The recipe with this id does not exist"


@pytest.mark.anyio
async def test_recipe_create(procedures):
    from baking.routers.recipe.models import RecipeCreate, RecipeRead
    recipe = RecipeCreate(
        name="test",
        description="test",
        procedures=procedures,
    )
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/recipe", json=recipe.dict())
    assert response.status_code == 200
    assert response.json()["name"] == recipe.name
    assert response.json()["description"] == recipe.description
    assert len(response.json()["procedures"]) == len(recipe.procedures)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/recipe/{response.json()['_id']}")
    assert response.status_code == 200
    assert RecipeRead(**response.json()) == RecipeRead(**response.json())


@pytest.mark.anyio
async def test_recipe_update(recipe_factory):
    from baking.routers.recipe.models import RecipeUpdate, RecipeRead

    recipe = await recipe_factory.create_async()
    recipe_update = RecipeUpdate(name="test_update")
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(f"/recipe/{recipe.id}", json=recipe_update.dict(exclude_unset=True))
    assert response.status_code == 200
    assert response.json()["name"] == recipe_update.name

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/recipe/{recipe.id}")
    assert response.status_code == 200
    assert RecipeRead(**response.json()) == RecipeRead(**response.json())

@pytest.mark.anyio
async def test_recipe_delete(recipe_factory):
    from baking.routers.recipe.models import RecipeRead

    recipe = await recipe_factory.create_async()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(f"/recipe/{recipe.id}")
    assert response.status_code == 200
    assert RecipeRead(**response.json()) == recipe

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/recipe/{recipe.id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "The recipe with this id does not exist"

@pytest.mark.anyio
async def test_recipe_delete_invalid_id(recipe_factory):
    from baking.routers.recipe.models import RecipeRead

    _: RecipeRead = await recipe_factory.create_async()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete("/recipe/abc")
        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid recipe id"

@pytest.mark.anyio
async def test_recipe_delete_not_found(recipe_factory):
    from baking.routers.recipe.models import RecipeRead

    _: RecipeRead = await recipe_factory.create_async()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(f"/recipe/644016caff25afc6b20de505")
    assert response.status_code == 404
    assert response.json()["detail"] == "The recipe with this id does not exist"

@pytest.mark.anyio
async def test_recipe_update_recipe_img(recipe_factory):
    from baking.routers.recipe.models import RecipeUpdate, RecipeRead

    recipe = await recipe_factory.create_async()
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(parent_dir + "/test_data/test.jpeg", "rb") as image_file:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            # mock the method baking.utils.azure_storage.upload_image_to_blob
            with patch("baking.utils.azure_storage.upload_image_to_blob") as mock_upload_image_to_blob:
                mock_upload_image_to_blob.return_value = 'bar'
                response = await ac.post(f"/recipe/{recipe.id}/img", files={"file": image_file})
    assert response.status_code == 200
    assert response.json()["file_path"] == "test.jpeg"

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/recipe/{recipe.id}")
    assert response.status_code == 200
    r_test = RecipeRead(**response.json())
    assert r_test.image


