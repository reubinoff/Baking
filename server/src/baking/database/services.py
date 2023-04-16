import json
import logging
import pymongo
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from baking.models import FilterCriteria, FilterOperator

from fastapi import Depends, Query

from pydantic.error_wrappers import ErrorWrapper, ValidationError
from pydantic import BaseModel
from pydantic.types import Json, constr

from baking.exceptions import (
    FieldNotFound,
    FieldNotFoundError,
    BadFilterFormat,
    InvalidFilterError,
)
from .manage import get_db

LOGGER = logging.getLogger(__name__)

def common_parameters(
    db_session: AsyncIOMotorDatabase = Depends(get_db),
    page: int = Query(1, gt=0, lt=2147483647),
    items_per_page: int = Query(5, alias="itemsPerPage", gt=-2, lt=2147483647),
    sort_by: List[str] = Query([], alias="sortBy[]"),
    descending: List[bool] = Query([], alias="descending[]"),
    filter_spec: Json = Query([], alias="filter"),

):

    return {
        "db_session": db_session,
        "page": page,
        "items_per_page": items_per_page,
        "sort_by": sort_by,
        "descending": descending,
        "filter_spec": filter_spec,
    }


async def search_filter_sort_paginate(
    db: AsyncIOMotorDatabase,
    *,
    collection_name: str,
    filter_criteria: List[FilterCriteria] = Query([]),
    page: int = 1,
    items_per_page: int = 5,
    sort_by: str = "",
    descending: bool = False,
    # current_user: DispatchUser = None,
    # role: UserRoles = UserRoles.member,
):
    """Common functionality for searching, filtering, sorting, and pagination."""
    # Build the MongoDB filter criteria based on the provided parameters
    validate_filter_spec(filter_criteria)
    filter_query = {}
    for criteria in filter_criteria:
        filter_query[criteria.name] = {f"{criteria.operator}": criteria.value}

    # Connect to the MongoDB server and perform the search
    collection = db[collection_name]

    results = collection.find(filter_query)
    # Apply sorting if requested
    if sort_by:
        sort_order = pymongo.DESCENDING if descending else pymongo.ASCENDING
        sort_criteria = [(sort_by, sort_order)]
        results = results.sort(sort_criteria)

    # Apply pagination if requested
    total_items = await collection.count_documents(filter_query)
    offset = (page - 1) * items_per_page
    results = results.skip(offset).limit(items_per_page)

    # Return the search results
    return {
        "total": total_items,
        "itemsPerPage": items_per_page,
        "page": page,
        "items": await results.to_list(length=items_per_page),
    }





def validate_filter_spec(filter_spec: List[dict]):
    """
    Validate the filter_spec parameter to ensure that all criteria are well-formed.
    Raises an InvalidFilterError with a 400 status code if any criteria are invalid.
    """
    if not isinstance(filter_spec, list):
        raise InvalidFilterError(
            status_code=400, detail="Invalid filter: filter is not a list")
    for criteria in filter_spec:
        if not getattr(criteria, "name") or not getattr(criteria, "value") or not getattr(criteria, "operator"):
            raise InvalidFilterError(
                status_code=400, detail="Invalid filter criteria: missing name, value, or operator")
        if not isinstance(criteria.name, str) or not isinstance(criteria.value, str) or not isinstance(criteria.operator, str):
            raise InvalidFilterError(
                status_code=400, detail="Invalid filter criteria: name, value, or operator is not a string")
        try:
            operator = FilterOperator(criteria.operator)
        except ValueError:
            raise InvalidFilterError(
                status_code=400, detail=f"Invalid filter criteria operator: {criteria.operator}")
