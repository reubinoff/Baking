import pytest
import asyncio
from httpx import AsyncClient
from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory import Use
from polyfactory.pytest_plugin import register_fixture


from baking.routers.recipe.models import RecipeCreate
from baking.routers.ingredients.models import IngredientType, IngredientUnits, IngredientCreate
from baking.routers.procedure.models import ProcedureCreate, Step
from baking.database.manage import drop_database, init_database
from baking.main import app

from .factories import AsyncPersistenceHandler


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", name="testapp")
def fixture_testapp():
    return app


@pytest.fixture(scope="function", autouse=True, name="database")
async def fixture_database():
    """
    Creates a new database 
    """
    mock_db = init_database()
    yield mock_db
    await drop_database()

@pytest.fixture(scope="function")
def client(testapp, database):
    testapp.db = database
    yield AsyncClient(app=testapp, base_url="http://test")


class StepFactory(ModelFactory[Step]):
    __model__ = Step
    description = Use(ModelFactory.__random__.choice, ['why am description_' + str(i) for i in range(100)])
    duration_in_seconds = Use(ModelFactory.__random__.randint, 1, 10000)
    
class IngredientFactory(ModelFactory[IngredientCreate]):
    __model__ = IngredientCreate

    name = Use(ModelFactory.__random__.choice, [
               'ingredient_' + str(i) for i in range(100)])
    quantity = Use(ModelFactory.__random__.randint, 1, 10000)
    units = Use(ModelFactory.__random__.choice, list(map(str, IngredientUnits)))
    type = Use(ModelFactory.__random__.choice, list(map(str, IngredientType)))


class ProcedureFactory(ModelFactory[ProcedureCreate]):
    """Procedure Factory."""
    __model__ = ProcedureCreate

    name = Use(ModelFactory.__random__.choice, ['procedure_' + str(i) for i in range(100)])
    ingredients = Use(IngredientFactory.batch, 3)
    steps = Use(StepFactory.batch, 3)

@register_fixture
class RecipeFactory(ModelFactory[RecipeCreate]):
    """Recipe Factory."""
    __model__ = RecipeCreate
    __async_persistence__ = AsyncPersistenceHandler()

    name = Use(ModelFactory.__random__.choice, ['recipe_' + str(i) for i in range(100)])
    description = Use(ModelFactory.__random__.choice, ['why am description_' + str(i) for i in range(100)])
    procedures = Use(ProcedureFactory.batch, 2)


@pytest.fixture(scope="function")
def procedures():
    return ProcedureFactory.batch(2)


@pytest.fixture(scope="function")
def procedure():
    return ProcedureFactory().build()


@pytest.fixture(scope="function")
def steps():
    return ProcedureFactory().batch(4)
