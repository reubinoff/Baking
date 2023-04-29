
import pytest
import asyncio
from starlette.testclient import TestClient

from .mongo_db import mongo_db

from baking.routers.recipe.models import RecipeCreate
from baking.routers.ingredients.models import IngrediantType, IngrediantUnits, IngredientCreate
from baking.routers.procedure.models import ProcedureCreate, Step

from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory import Use
from polyfactory.pytest_plugin import register_fixture



from .factories import AsyncPersistenceHandler


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()

def pytest_runtest_setup(item):
    if "slow" in item.keywords and not item.config.getoption("--runslow"):
        pytest.skip("need --runslow option to run")

    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail("previous test failed ({0})".format(previousfailed.name))


def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item


@pytest.fixture(scope="function", autouse=True)
async def database():
    """
    Creates a new database 
    """
    from baking.database.manage import drop_database, init_database
    mock_db = init_database()
    yield mock_db
    await drop_database()
    
    


@pytest.fixture(scope="function")
def client(testapp):
    yield TestClient(testapp)


class StepFactory(ModelFactory[Step]):
    __model__ = Step

    name = Use(ModelFactory.__random__.choice, ['step_' + str(i) for i in range(100)])
    description = Use(ModelFactory.__random__.choice, ['why am description_' + str(i) for i in range(100)])
    duration_in_seconds = Use(ModelFactory.__random__.randint, 1, 10000)
    
class IngredientFactory(ModelFactory[IngredientCreate]):
    __model__ = IngredientCreate

    name = Use(ModelFactory.__random__.choice, [
               'ingredient_' + str(i) for i in range(100)])
    quantity = Use(ModelFactory.__random__.randint, 1, 10000)
    units = Use(ModelFactory.__random__.choice, list(map(str, IngrediantUnits)))
    type = Use(ModelFactory.__random__.choice, list(map(str, IngrediantType)))


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
    pass


@pytest.fixture(scope="function")
def procedures():
    return ProcedureFactory.batch(2)


@pytest.fixture(scope="function")
def procedure():
    return ProcedureFactory().build()


@pytest.fixture(scope="function")
def steps():
    return ProcedureFactory().batch(4)
