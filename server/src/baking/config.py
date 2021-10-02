import os

from typing import Any, Optional

from pydantic import BaseSettings


CONFIG_NAME: str = os.environ.get("CONFIG_NAME", ".env")


class BakingConfig(BaseSettings):
    service_name: str

    log_level: str = "INFO"

    db_host: str
    db_pass: str
    db_name: str
    db_user: str
    db_cert_path: str = ""
    db_debug_drop_in_startup: bool = False

    alembix_ini = (f"{os.path.dirname(os.path.realpath(__file__))}/alembic.ini",)

    class Config:
        env_file = CONFIG_NAME


settings = BakingConfig()
