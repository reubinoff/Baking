import logging
from motor.motor_asyncio import AsyncIOMotorClient 
from functools import lru_cache

from starlette.requests import Request
from baking.config import settings as app_settings

from baking.config import settings


LOGGER = logging.getLogger(__name__)


@lru_cache
def get_sql_url() -> str:
    return f"mongodb://{app_settings.db_user}:{app_settings.db_pass}@{app_settings.db_host}:27017/"


def get_db(request: Request):
    return request.state.db[app_settings.db_name]


def get_client() -> AsyncIOMotorClient:
    return AsyncIOMotorClient(get_sql_url())

def init_database():
    """Initializes a the database."""
    LOGGER.debug(f"conn str: {get_sql_url()}")
    # check if mongiodb exists
    mongo_client: AsyncIOMotorClient = get_client()
    if app_settings.db_name not in mongo_client.list_database_names():
        #create db
        mongo_client[app_settings.db_name]

    elif settings.db_debug_drop_in_startup is True:
        mongo_client.drop_database(app_settings.db_name)
        mongo_client[app_settings.db_name]


