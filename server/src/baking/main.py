
from fastapi import FastAPI
from fastapi.logger import logger

from baking.config import get_config
from baking.logger import init_logger
from baking.router import api_router
from baking.exceptions import base_error_handler


init_logger()

app = FastAPI()
app.include_router(api_router)
app.add_exception_handler(Exception, base_error_handler)


logger.info(f"Start service: {get_config().service_name}")
