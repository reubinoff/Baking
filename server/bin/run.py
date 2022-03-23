import logging
import uvicorn
import os

from alembic import command as alembic_command
from alembic.config import Config as AlembicConfig

from src.baking.config import settings
from src.baking.database.manage import internal_create_database_for_tests
from src.baking.database.core import engine

if __name__ == "__main__":
    internal_create_database_for_tests(engine=engine)
    revision = "head" 
    alembic_cfg = AlembicConfig(settings.alembix_ini)
    alembic_cfg.set_main_option("script_location", settings.revisions_location)
    alembic_command.upgrade(alembic_cfg, revision)
    print("Migration ended")
    uvicorn.run(
        "src.baking.main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8888")),
        log_level=logging.DEBUG,
    )
