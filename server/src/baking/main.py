from fastapi import FastAPI
from fastapi.logger import logger

from baking.config import settings
from baking.logger import init_logger
from baking.router import api_router
from baking.exceptions import base_error_handler
from baking.middlewares import get_middlewares
from baking.database.manage import init_database
from baking.database.core import engine

init_logger()

init_database(engine=engine)

app = FastAPI(middleware=get_middlewares())
app.include_router(api_router)
app.add_exception_handler(Exception, base_error_handler)


logger.info(f"Start service: {settings.service_name}")
