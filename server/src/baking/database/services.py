import json

from typing import List

from fastapi import Depends, Query
from fastapi.logger import logger
import sqlalchemy

from sqlalchemy import or_, orm, func, desc
from sqlalchemy_filters import apply_pagination, apply_sort, apply_filters
from pydantic.error_wrappers import ErrorWrapper, ValidationError
from pydantic import BaseModel
from pydantic.types import Json, constr

from baking.exceptions import (
    FieldNotFound,
    FieldNotFoundError,
    BadFilterFormat,
    InvalidFilterError,
)

from .core import (
    Base,
    get_class_by_tablename,
    get_model_name_by_tablename,
    get_db,
)

QueryStr = constr(regex=r"^[ -~\u0590-\u05FF\u200f\u200e ]+$", min_length=1)


def common_parameters(
    db_session: orm.Session = Depends(get_db),
    page: int = Query(1, gt=0, lt=2147483647),
    items_per_page: int = Query(5, alias="itemsPerPage", gt=-2, lt=2147483647),
    sort_by: List[str] = Query([], alias="sortBy[]"),
    descending: List[bool] = Query([], alias="descending[]"),
    query_str: QueryStr = Query(None, alias="q"),

):

    return {
        "db_session": db_session,
        "page": page,
        "items_per_page": items_per_page,
        "sort_by": sort_by,
        "descending": descending,
        "query_str": query_str
    }


def search(*, query_str: str, query: orm.Query, model: str, sort=False):
    """Perform a search based on the query."""
    search_model = get_class_by_tablename(model)

    if not query_str.strip():
        return query

    vector = search_model.search_vector

    query = query.filter(vector.op("@@")(func.tsq_parse(query_str)))
    if sort:
        query = query.order_by(desc(func.ts_rank_cd(vector, func.tsq_parse(query_str))))

    return query.params(term=query_str)


def create_sort_spec(model, sort_by, descending):
    """Creates sort_spec."""
    sort_spec = []
    if sort_by and descending:
        for field, direction in zip(sort_by, descending):
            direction = "desc" if direction else "asc"

            # we have a complex field, we may need to join
            if "." in field:
                complex_model, complex_field = field.split(".")[-2:]

                sort_spec.append(
                    {
                        "model": get_model_name_by_tablename(complex_model),
                        "field": complex_field,
                        "direction": direction,
                    }
                )
            else:
                sort_spec.append(
                    {"model": model, "field": field, "direction": direction}
                )
    logger.debug(f"Sort Spec: {json.dumps(sort_spec, indent=2)}")
    return sort_spec


def search_filter_sort_paginate(
    db_session,
    model,
    query_str: str = None,
    page: int = 1,
    items_per_page: int = 5,
    sort_by: List[str] = None,
    descending: List[bool] = None,
    # current_user: DispatchUser = None,
    # role: UserRoles = UserRoles.member,
):
    """Common functionality for searching, filtering, sorting, and pagination."""
    if db_session is None:
        return
    model_cls = get_class_by_tablename(model)
    try:
        query = db_session.query(model_cls)


        if query_str:
            sort = False if sort_by else True
            query = search(query_str=query_str, query=query,
                    model=model, sort=sort)

        if sort_by is not None and isinstance(sort_by, List) and len(sort_by) > 0:
            # print(sort_by)
            sort_spec = create_sort_spec(model, sort_by, descending)
            query = apply_sort(query, sort_spec)

    except FieldNotFound as e:
        raise ValidationError(
            [
                ErrorWrapper(FieldNotFoundError(msg=str(e)), loc="filter"),
            ],
            model=BaseModel,
        )
    except BadFilterFormat as e:
        raise ValidationError(
            [ErrorWrapper(InvalidFilterError(msg=str(e)), loc="filter")],
            model=BaseModel,
        )

    except AttributeError as e:
        raise ValidationError(
            [
                ErrorWrapper(FieldNotFoundError(msg=str(e)), loc="filter"),
            ],
            model=BaseModel,
        )

    if items_per_page == -1:
        items_per_page = None

    # sometimes we get bad input for the search function
    # TODO investigate moving to a different way to parsing queries that won't through errors
    # e.g. websearch_to_tsquery
    # https://www.postgresql.org/docs/current/textsearch-controls.html
    try:
        query, pagination = apply_pagination(
            query, page_number=page, page_size=items_per_page
        )
    except sqlalchemy.exc.ProgrammingError as e:
        logger.debug(e)
        return {
            "items": [],
            "itemsPerPage": items_per_page,
            "page": page,
            "total": 0,
        }

    return {
        "items": query.all(),
        "itemsPerPage": pagination.page_size,
        "page": pagination.page_number,
        "total": pagination.total_results,
    }
