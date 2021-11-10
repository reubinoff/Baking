import pytest
import random
from sqlalchemy_utils import drop_database
from starlette.testclient import TestClient
from starlette.config import environ

from factory import Sequence

# set test config
environ["DB_PASS"] = "rootsql"
environ["DB_HOST"] = "127.0.0.1"
environ["DB_NAME"] = "baking-db-test-" + str(random.random())
environ["DB_USER"] = "postgres"


from baking import config
from baking.database.core import engine, get_sql_url
from baking.database.manage import init_database


from .factories import IngredientFactory, ProcedureFactory, RecipeFactory

from .database import Session


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


@pytest.fixture(scope="session")
def db():
    init_database(engine)
    Session.configure(bind=engine)
    yield
    drop_database(get_sql_url())


@pytest.fixture(scope="function", autouse=True)
def session(db):
    """
    Creates a new database session with (with working transaction)
    for test duration.
    """
    session = Session()
    session.begin_nested()
    yield session
    session.rollback()


@pytest.fixture(scope="function")
def client(testapp, session, client):
    yield TestClient(testapp)


@pytest.fixture
def recipe(session):
    return RecipeFactory()


@pytest.fixture
def recipes(session):
    return [RecipeFactory(), RecipeFactory()]


@pytest.fixture
def ingredient(session):
    return IngredientFactory()


@pytest.fixture
def ingredients(session):
    return [IngredientFactory(), IngredientFactory()]


@pytest.fixture
def procedure(session):
    return ProcedureFactory()


@pytest.fixture
def procedures(session):
    return [ProcedureFactory(), ProcedureFactory(), ProcedureFactory()]
