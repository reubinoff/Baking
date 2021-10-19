import re
import functools
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker, object_session
from sqlalchemy.sql.expression import true
from sqlalchemy_utils import get_mapper, get_class_by_table
from starlette.requests import Request

from baking.config import settings as app_settings

CERT_PATH = (
    None if app_settings.db_cert_path == "" else {"ssl_ca": app_settings.db_cert_path}
)
SQL_URI = URL.create(
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

    @classmethod
    def model_lookup_by_table_name(cls, table_name):
        registry_instance = getattr(cls, "registry")
        for mapper_ in registry_instance.mappers:
            model = mapper_.class_
            model_class_name = model.__tablename__
            if model_class_name == table_name.lower():
                return model


Base = declarative_base(cls=CustomBase)


def get_db(request: Request):
    return request.state.db


def get_model_name_by_tablename(table_fullname: str) -> str:
    """Returns the model name of a given table."""
    obj = get_class_by_tablename(table_fullname=table_fullname)
    return obj.__name__ if obj is not None else None


def get_class_by_tablename(table_fullname: str) -> Any:
    """Return class reference mapped to table."""
    try:
        mapped_class = Base.model_lookup_by_table_name(table_fullname)
    except:
        return None
    return mapped_class
