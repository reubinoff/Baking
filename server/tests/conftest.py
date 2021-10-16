import pytest

from sqlalchemy_utils import drop_database
from starlette.testclient import TestClient
from starlette.config import environ


# set test config
environ["DB_PASS"] = "sql"
environ["DB_HOST"] = "mysql"
environ["DB_NAME"] = "ttt"
environ["DB_USER"] = "test"


from baking import config
from baking.database.core import engine, SQL_URI
from baking.database.manage import init_database


from .factories import RecipeFactory

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
    drop_database(str(SQL_URI))


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
