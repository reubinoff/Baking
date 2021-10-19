import logging

from fastapi import FastAPI


from baking.config import settings
from baking.logger import init_logger
from baking.router import api_router
from baking.exceptions import base_error_handler
from baking.middlewares import get_middlewares
from baking.database.manage import init_database
from baking.database.core import engine


init_logger()
logger = logging.getLogger(__name__)

init_database(engine=engine)


app = FastAPI(
    title="Baking Hub",
    description="Hub for great bread recipes",
    version="0.2.1",
    middleware=get_middlewares(),
    openapi_url="/docs/openapi.json",
)
app.include_router(api_router)
app.add_exception_handler(Exception, base_error_handler)


logger.info(f"Start service: {settings.service_name}")
logger.info(f"db host: {settings.db_host}")
