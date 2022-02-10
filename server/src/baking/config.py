import os

from pydantic import BaseSettings
class BakingConfig(BaseSettings):
    service_name: str = "testing-service"  # will be replaced in env var

    log_level: str = "INFO"

    db_host: str
    db_pass: str
    db_name: str
    db_user: str
    db_cert_path: str = ""
    db_debug_drop_in_startup: bool = False

    alembix_ini = f"{os.path.dirname(os.path.realpath(__file__))}/alembic.ini"

    root_path = ""


settings = BakingConfig()
