import re
import functools
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker, object_session
from sqlalchemy.sql.expression import true
from sqlalchemy_utils import get_mapper
from starlette.requests import Request

from baking.config import settings as app_settings

CERT_PATH = (
    None if app_settings.db_cert_path == "" else {"ssl_ca": app_settings.db_cert_path}
)
SQL_URI = URL(
    drivername="mysql+pymysql",
    username=app_settings.db_user,
    password=app_settings.db_pass,
    host=app_settings.db_host,
    port=3306,
    database=app_settings.db_name,
    query=CERT_PATH,
)

engine = create_engine(str(SQL_URI))
SessionLocal = sessionmaker(bind=engine)


def resolve_table_name(name):
    """Resolves table names to their mapped names."""
    names = re.split("(?=[A-Z])", name)  # noqa
    return "_".join([x.lower() for x in names if x])


class CustomBase:
    @declared_attr
    def __tablename__(self):
        return resolve_table_name(self.__name__)

    def dict(self):
        """Returns a dict representation of a model."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


Base = declarative_base(cls=CustomBase)


def get_db(request: Request):
    return request.state.db


def get_model_name_by_tablename(table_fullname: str) -> str:
    """Returns the model name of a given table."""
    return get_class_by_tablename(table_fullname=table_fullname).__name__


def get_class_by_tablename(table_fullname: str) -> Any:
    """Return class reference mapped to table."""

    def _find_class(name):
        for c in Base._decl_class_registry.values():
            if hasattr(c, "__table__"):
                if c.__table__.fullname.lower() == name.lower():
                    return c

    mapped_name = resolve_table_name(table_fullname)
    mapped_class = _find_class(mapped_name)

    # try looking in the '' schema
    if not mapped_class:
        mapped_class = _find_class(f"{app_settings.db_name}.{mapped_name}")

    if not mapped_class:
        raise Exception(
            f"Incorrect tablename '{mapped_name}'. Check the name of your model."
        )

    return mapped_class
