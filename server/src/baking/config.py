import os

from typing import Any, Optional

from pydantic import BaseSettings


class BakingConfig(BaseSettings):
    service_name: str

    db_host: str
    db_pass: str
    db_name: str

    alembix_ini = (f"{os.path.dirname(os.path.realpath(__file__))}/alembic.ini",)

    class Config:
        env_file = ".env"


settings = BakingConfig()
