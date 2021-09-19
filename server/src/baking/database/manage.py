from sqlalchemy.schema import CreateSchema

from sqlalchemy_utils import create_database, database_exists
from alembic.config import Config as AlembicConfig
from alembic import command as alembic_command

from fastapi_best_practice.config import configuration

from .core import Base, sessionmaker,SQL_URI

def version_schema(script_location: str):
    """Applies alembic versioning to schema."""

    # add it to alembic table
    alembic_cfg = AlembicConfig(configuration.alembix_ini)
    alembic_cfg.set_main_option("script_location", script_location)
    alembic_command.stamp(alembic_cfg, "head")

def get_core_tables():
    return [table for _, table in Base.metadata.tables.items()]


def init_database(engine):
    """Initializes a the database."""
    if not database_exists(str(SQL_URI)):
        create_database(str(SQL_URI))

    schema_name = configuration.db_name
    with engine.connect() as connection:
        if schema_name not in connection.dialect.get_schema_names(connection):
            connection.execute(CreateSchema(schema_name))
        
    tables = get_core_tables()

    Base.metadata.create_all(engine, tables=tables)

  
