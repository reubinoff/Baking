import pytest
import schemathesis
from fastapi.testclient import TestClient
from schemathesis.checks import ALL_CHECKS, DEFAULT_CHECKS
from httpx import AsyncClient

from hypothesis import settings, HealthCheck

from baking.main import app


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