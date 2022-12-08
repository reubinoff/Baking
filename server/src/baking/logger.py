import logging
import colorlog
import sys
from baking.config import settings
import logging.config

LOGGING =  {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'logzioFormat': {
            'format': '{"additional_field": "value"}',
            'validate': False
        }
    },
    'handlers': {
        'logzio': {
            'class': 'logzio.handler.LogzioHandler',
            'level': "INFO",
            'formatter': 'logzioFormat',
            'token': settings.logzio_token,
            'logzio_type': 'python',
            'logs_drain_timeout': 5,
            'url': 'https://listener-uk.logz.io:8071',
        }
    },
    'loggers': {
        '': {
            'level': settings.log_level,
            'handlers': ['logzio'],
            'propagate': True
        }
    }
}

def init_logger():
    if settings.logzio_token:
        logging.config.dictConfig(LOGGING)

    handler = logging.StreamHandler(stream=sys.stdout)

    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.info('Logger initated!')
