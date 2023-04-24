import logging
import sys
from baking.config import settings
import logging.config


def init_logger():
    handler = logging.StreamHandler(stream=sys.stdout)

    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.info('Logger initated!')
