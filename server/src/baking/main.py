import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI


from baking.config import settings
from baking.logger import init_logger
from baking.router import api_router
from baking.exceptions import base_error_handler
from baking.middlewares import get_middlewares
from baking.database.manage import init_database


init_logger()
db = init_database()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def startup_event(fastapi_app: FastAPI):
    fastapi_app.db = db
    yield

# base_path = f"/{settings.root_path}" if settings.root_path else ""
app = FastAPI(
    title="Baking Hub",
    description="Hub for great bread recipes",
    version="0.2.2",
    middleware=get_middlewares(),
    docs_url=None if settings.is_debug is False else "/docs",
    openapi_url=None if settings.is_debug is False else "/docs/openapi.json",

    root_path=f"{settings.root_path}",
    lifespan=startup_event
)
app.include_router(api_router)
app.add_exception_handler(Exception, base_error_handler)


logger.info(f"Debug mode is : {settings.is_debug}")
logger.info(f"Start service: {settings.service_name}")
