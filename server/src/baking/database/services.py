import json

from typing import List

from fastapi import Depends, Query
from fastapi.logger import logger

from sqlalchemy import or_, orm, func, desc
from sqlalchemy_filters import apply_pagination, apply_sort, apply_filters


from .core import (
    Base,
    get_class_by_tablename,
    get_model_name_by_tablename,
    get_db,
)

def common_parameters(
    db_session: orm.Session = Depends(get_db),
    page: int = 1,
    items_per_page: int = Query(5, alias="itemsPerPage"),
    query_str: str = Query(None, alias="q"),
    filter_spec: str = Query([], alias="filter"),
    sort_by: List[str] = Query([], alias="sortBy[]"),
    descending: List[bool] = Query([], alias="descending[]"),
):
    if filter_spec:
        filter_spec = json.loads(filter_spec)

    return {
        "db_session": db_session,
        "page": page,
        "items_per_page": items_per_page,
        "query_str": query_str,
        "filter_spec": filter_spec,
        "sort_by": sort_by,
        "descending": descending,
    }


def search(*, query_str: str, query: Query, model: str, sort=False):
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
                sort_spec.append({"model": model, "field": field, "direction": direction})
    logger.debug(f"Sort Spec: {json.dumps(sort_spec, indent=2)}")
    return sort_spec



def search_filter_sort_paginate(
    db_session,
    model,
    query_str: str = None,
    filter_spec: List[dict] = None,
    page: int = 1,
    items_per_page: int = 5,
    sort_by: List[str] = None,
    descending: List[bool] = None,
):
    """Common functionality for searching, filtering, sorting, and pagination."""
    model_cls = get_class_by_tablename(model)
    sort_spec = create_sort_spec(model, sort_by, descending)

    query = db_session.query(model_cls)

    if query_str:
        sort = False if sort_by else True
        query = search(query_str=query_str, query=query, model=model, sort=sort)

    if filter_spec:
        query = apply_filters(query, filter_spec)

    query = apply_sort(query, sort_spec)

    if items_per_page == -1:
        items_per_page = None

    query, pagination = apply_pagination(query, page_number=page, page_size=items_per_page)

    return {
        "items": query.all(),
        "itemsPerPage": pagination.page_size,
        "page": pagination.page_number,
        "total": pagination.total_results,
    }
