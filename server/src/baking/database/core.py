import re
from typing import Any
from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy import URL

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import sessionmaker, declarative_base, configure_mappers
from starlette.requests import Request

from baking.config import settings as app_settings
from baking.search.fulltext import make_searchable


@lru_cache
def get_sql_url() -> URL:
    return URL.create(
        "postgresql+psycopg2",
        username=app_settings.db_user,
        password=app_settings.db_pass,
        host=app_settings.db_host,
        database=app_settings.db_name,
    )


engine = create_engine(get_sql_url())
configure_mappers()  # IMPORTANT!



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
make_searchable(Base.metadata)


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
