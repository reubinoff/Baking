import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from functools import lru_cache

from starlette.requests import Request
from baking.config import settings as app_settings

from baking.config import settings


LOGGER = logging.getLogger(__name__)


@lru_cache
def get_sql_url() -> str:
    return f"mongodb://{app_settings.db_user}:{app_settings.db_pass}@{app_settings.db_host}:27017/"


def get_db(request: Request):
    return request.app.db

def init_database() -> AsyncIOMotorDatabase:
    """Initializes a the database."""
    db = None
    LOGGER.debug(f"conn str: {get_sql_url()}")
    # check if mongiodb exists
    mongo_client: AsyncIOMotorClient = AsyncIOMotorClient(get_sql_url())
   
    db = mongo_client[app_settings.db_name]

    if settings.db_debug_drop_in_startup is True:
        mongo_client.drop_database(app_settings.db_name)
        mongo_client[app_settings.db_name]
    return db


async def drop_database():
    """Drops the database."""
    mongo_client: AsyncIOMotorClient = AsyncIOMotorClient(get_sql_url())
    await mongo_client.drop_database(app_settings.db_name)
