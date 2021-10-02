import logging
import colorlog

from fastapi import logger

from baking.config import settings


def init_logger():
    if settings.log_level == "DEBUG":
        handler = colorlog.StreamHandler()
        handler.setFormatter(
            colorlog.ColoredFormatter("%(log_color)s%(levelname)s:%(name)s:%(message)s")
        )
        handler.setLevel(settings.log_level)

        logger = colorlog.getLogger("baking")
        logger.addHandler(handler)

    else:
        logging.basicConfig(level=settings.log_level)
