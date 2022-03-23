import logging

from sqlalchemy.schema import CreateSchema

from sqlalchemy_utils import create_database, database_exists
from alembic.config import Config as AlembicConfig
from alembic import command as alembic_command

from baking.config import settings

from .core import Base, get_sql_url

LOGGER = logging.getLogger(__name__)


def version_schema(script_location: str):
    """Applies alembic versioning to schema."""

    # add it to alembic table
    alembic_cfg = AlembicConfig(settings.alembix_ini)
    alembic_cfg.set_main_option("script_location", script_location)
    alembic_command.stamp(alembic_cfg, "head")


def get_tables():
    return [table for _, table in Base.metadata.tables.items()]


def init_database(engine):
    """Initializes a the database."""
    LOGGER.info(f"conn str: {get_sql_url()}")
    required_tables_creation = False
    if database_exists(get_sql_url()) is False:
        raise Exception("No database exists")
        # create_database(get_sql_url())
        # required_tables_creation = True

    schema_name = settings.db_name
    with engine.connect() as connection:
        if schema_name not in connection.dialect.get_schema_names(connection):
            connection.execute(CreateSchema(schema_name))

    tables = get_tables()

    if settings.db_debug_drop_in_startup is True or required_tables_creation is True:
        Base.metadata.drop_all(engine, tables=tables)
        Base.metadata.create_all(engine, tables=tables)


def internal_create_database_for_tests(engine):
    create_database(get_sql_url())
    schema_name = settings.db_name
    with engine.connect() as connection:
        if schema_name not in connection.dialect.get_schema_names(connection):
            connection.execute(CreateSchema(schema_name))
    tables = get_tables()
    Base.metadata.drop_all(engine, tables=tables)
    Base.metadata.create_all(engine, tables=tables)