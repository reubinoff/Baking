import os
import logging

from sqlalchemy.schema import CreateSchema
from sqlalchemy import text

from sqlalchemy_utils import create_database, database_exists
from alembic.config import Config as AlembicConfig
from alembic import command as alembic_command

from baking.config import settings
from baking.search.fulltext import sync_trigger
from baking.search import fulltext

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
    # LOGGER.debug(f"conn str: {get_sql_url()}")
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
    setup_fulltext_search(engine, tables)


    if settings.db_debug_drop_in_startup is True or required_tables_creation is True:
        Base.metadata.drop_all(engine, tables=tables)
        Base.metadata.create_all(engine, tables=tables)


def internal_create_database_for_tests(engine):
    if database_exists(get_sql_url()) is False:
        create_database(engine.url)
    schema_name = settings.db_name
    with engine.connect() as connection:
        if schema_name not in connection.dialect.get_schema_names(connection):
            connection.execute(CreateSchema(schema_name))
    tables = get_tables()
    Base.metadata.drop_all(engine, tables=tables)
    Base.metadata.create_all(engine, tables=tables)



def setup_fulltext_search(connection, tables):
    """Syncs any required fulltext table triggers and functions."""
    # parsing functions
    function_path = os.path.join(
        os.path.dirname(os.path.abspath(fulltext.__file__)), "expressions.sql"
    )

    with connection.connect() as conn:
        result = conn.execute(text(open(function_path).read()))

    for table in tables:
        table_triggers = []
        for column in table.columns:
            if column.name.endswith("search_vector"):
                if hasattr(column.type, "columns"):
                    table_triggers.append(
                        {
                            "conn": connection,
                            "table": table,
                            "tsvector_column": "search_vector",
                            "indexed_columns": column.type.columns,
                        }
                    )
                else:
                    LOGGER.warning(
                        f"Column search_vector defined but no index columns found. Table: {table.name}"
                    )

        for trigger in table_triggers:
            print(f"{trigger}")
            sync_trigger(**trigger)
