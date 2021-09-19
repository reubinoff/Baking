# -*- coding: utf-8 -*-
from functools import lru_cache
from typing import Any, Optional

from pydantic import BaseSettings


class BakingConfig(BaseSettings):
    service_name: str
    

    class Config:
        env_file = ".env"


@lru_cache()
def get_config():
    settings = BakingConfig()
    return settings
