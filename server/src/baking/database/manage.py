import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from functools import lru_cache
from pymongo import MongoClient, TEXT

from starlette.requests import Request
from baking.config import settings as app_settings

from baking.config import settings


LOGGER = logging.getLogger(__name__)

INDEXES = {
    "recipes": ["name", "description"],
}

@lru_cache
def get_sql_url() -> str:
    return f"{app_settings.db_conn_str}"


def get_db(request: Request):
    return request.app.db

def init_database() -> AsyncIOMotorDatabase:
    """Initializes a the database."""
    db = None
    LOGGER.debug(f"conn str: {get_sql_url()}")
    # check if mongiodb exists
    mongo_client: AsyncIOMotorClient = AsyncIOMotorClient(get_sql_url())
    try:
        db = mongo_client[app_settings.db_name]
        _configure_indexes()
    except Exception as e:
        LOGGER.error(f"Database {app_settings.db_name} does not exist")
        raise e

    if settings.db_debug_drop_in_startup is True:
        mongo_client.drop_database(app_settings.db_name)
        mongo_client[app_settings.db_name]
    return db

def _configure_indexes():
    """Configures the database indexes."""
    mongo_client = MongoClient(get_sql_url(), connect=True)
    db = mongo_client[app_settings.db_name]
    for collection_name, indexes in INDEXES.items():
        # create dic of index: "text"
        indexes = [(index, TEXT) for index in indexes]
        a = db[collection_name].create_index(indexes)
    return True
        


    

async def drop_database():
    """Drops the database."""
    mongo_client: AsyncIOMotorClient = AsyncIOMotorClient(get_sql_url())
    await mongo_client.drop_database(app_settings.db_name)
