import json
import logging
import pymongo
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from baking.models import FilterCriteria, FilterOperator

from fastapi import Depends, Query
from typing import Annotated

from pydantic.types import Json

from baking.exceptions import (
    InvalidFilterError,
)
from .manage import get_db

LOGGER = logging.getLogger(__name__)

class CommonQueryParams:
    def __init__(   self,
                    page: Annotated[int, Query(alias="page", gt=0)] = 1, 
                    items_per_page: Annotated[int, Query(alias="itemsPerPage", gt=0, lt=200)] = 5,
                    sort_by: Annotated[str, Query(alias="sortBy")] = "",
                    descending: Annotated[bool, Query(alias="descending")] = False,
                    filter_criteria: Annotated[Json | None, Query(alias="filter")] = None,
                    ):
            self.page = page
            self.items_per_page = items_per_page
            self.sort_by = sort_by
            self.descending = descending
            self.filter_criteria = filter_criteria



async def search_filter_sort_paginate(
    db: AsyncIOMotorDatabase,
    *,
    collection_name: str,
    params: CommonQueryParams
    # current_user: DispatchUser = None,
    # role: UserRoles = UserRoles.member,
):
    """Common functionality for searching, filtering, sorting, and pagination."""
    # Build the MongoDB filter criteria based on the provided parameters
   
    filter_query = {}
    if params.filter_criteria:
        filter_obj_list = validate_filter_spec(params.filter_criteria)
        for criteria in filter_obj_list:
            filter_query[criteria.name] = {f"{criteria.operator}": criteria.value}

    # Connect to the MongoDB server and perform the search
    collection = db[collection_name]

    results = collection.find(filter_query)
    # Apply sorting if requested
    if params.sort_by:
        sort_order = pymongo.DESCENDING if params.descending else pymongo.ASCENDING
        sort_criteria = [(params.sort_by, sort_order)]
        results = results.sort(sort_criteria)

    # Apply pagination if requested
    total_items = await collection.count_documents(filter_query)
    offset = (params.page - 1) * params.items_per_page
    results = results.skip(offset).limit(params.items_per_page)

    # Return the search results
    return {
        "total": total_items,
        "itemsPerPage": params.items_per_page,
        "page": params.page,
        "items": await results.to_list(length=params.items_per_page),
    }


def validate_filter_spec(filter_spec: list) -> list[FilterCriteria]:
    """
    Validate the filter_spec parameter to ensure that all criteria are well-formed.
    Raises an InvalidFilterError with a 400 status code if any criteria are invalid.
    """
    if not filter_spec:
        return
    if not isinstance(filter_spec, list):
        raise InvalidFilterError(
            status_code=400, detail="Invalid filter: filter is not a list")
    filter_obj_list: list[FilterCriteria] = _cast_to_filter_Critiria_list(filter_spec)
    for criteria in filter_obj_list:
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
    return filter_obj_list


def _cast_to_filter_Critiria_list(filter_spec: list) -> list[FilterCriteria]:
    """
    Cast the filter_spec parameter to list of FilterCriteria.
    """
    if not filter_spec:
        return
    if not isinstance(filter_spec, list):
        filter_spec = json.loads(filter_spec)
    filter_obj_list: list[FilterCriteria] = []
    for criteria in filter_spec:
        if isinstance(criteria, dict):
            filter_obj_list.append(FilterCriteria(**criteria))
        elif isinstance(criteria, FilterCriteria):
            filter_obj_list.append(criteria)
    return filter_obj_list
