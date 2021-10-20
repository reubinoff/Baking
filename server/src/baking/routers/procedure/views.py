from baking.routers.ingredients.service import delete
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.logger import logger


from sqlalchemy.orm import Session


from baking.models import OurBase, PrimaryKey
from baking.database.core import get_db
from baking.database.services import common_parameters, search_filter_sort_paginate

from baking.routers.procedure.models import (
    ProcedureCreate,
    ProcedureRead,
    ProcedurePagination,
    ProcedureUpdate,
)
from baking.routers.procedure.service import create, get, update, delete

router = APIRouter()


@router.get("", response_model=ProcedurePagination)
def get_items(*, common: dict = Depends(common_parameters)):
    """
    Get all procedures.
    """
    return search_filter_sort_paginate(model="Procedure", **common)


@router.get("/{procedure_id}", response_model=ProcedureRead)
def get_procedure(*, db_session: Session = Depends(get_db), procedure_id: int):
    """
    Update a procedure.
    """
    procedure = get(db_session=db_session, procedure_id=procedure_id)
    if not procedure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "The procedure with this id does not exist."}],
        )
    return procedure


@router.post("", response_model=ProcedureRead)
def create_procedure(
    *, db_session: Session = Depends(get_db), procedure_in: ProcedureCreate
):
    """
    Create a new procedures.
    """
    procedure = create(db_session=db_session, procedure_in=procedure_in)
    return procedure


@router.delete("/{procedure_id}", response_model=ProcedureRead)
def delete_recipe(*, db_session: Session = Depends(get_db), procedure_id: PrimaryKey):
    """Delete a procedure."""
    procedure = get(db_session=db_session, procedure_id=procedure_id)
    if not procedure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "The procedure with this id does not exist."}],
        )
    delete(db_session=db_session, procedure_id=procedure_id)
    return procedure


@router.put("/{procedure_id}", response_model=ProcedureRead)
def update_recipe(
    *,
    db_session: Session = Depends(get_db),
    procedure_id: PrimaryKey,
    procedure_in: ProcedureUpdate
):
    """Update a procedure."""
    procedure = get(db_session=db_session, procedure_id=procedure_id)
    if not procedure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "The procedure with this id does not exist."}],
        )
    procedure = update(
        db_session=db_session, procedure=procedure, procedure_in=procedure_in
    )
    return procedure
