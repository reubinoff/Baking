from typing import Optional, List

from .models import ProcedureRead, ProcedureCreate, Procedure, ProcedureUpdate

from baking.routers.ingredients.service import (
    get_or_create as get_or_create_ingidient,
)

def get(*, db_session, procedure_id: int) -> Optional[Procedure]:
    """Returns a item based on the given Procedure id."""
    return (
        db_session.query(Procedure).filter(Procedure.id == procedure_id).one_or_none()
    )


def get_all(*, db_session) -> List[Optional[Procedure]]:
    """Returns all Procedures."""
    return db_session.query(Procedure).order_by(Procedure.order.desc())


def create(*, db_session, procedure_in: ProcedureCreate) -> Procedure:
    """Creates a new Procedure."""
    ingredients = []
    if procedure_in.ingredients is not None and isinstance(
        procedure_in.ingredients, List
    ):
        ingredients = [
            get_or_create_ingidient(db_session=db_session, ingredient_in=ingredient_in)
            for ingredient_in in procedure_in.ingredients
        ]
    steps = []
    if procedure_in.steps is not None and isinstance(
        procedure_in.steps, List
    ):
        steps = [
            get_or_create_step(db_session=db_session, step_in=step_in)
            for step_in in procedure_in.steps
        ]
    procedure = Procedure(
        **procedure_in.dict(exclude={"ingredients", "steps"})
    )

    db_session.add(procedure)
    procedure.steps = steps
    procedure.ingredients = ingredients
    db_session.commit()
    return procedure


def get_or_create(*, db_session, procedure_in: ProcedureCreate) -> Procedure:
    """Gets or creates a new procedure."""
    # prefer the Procedure id if available
    q = None
    if procedure_in.id:
        q = db_session.query(Procedure).filter(Procedure.id == procedure_in.id)

    # else:
    #     q = db_session.query(Procedure).filter_by(name=procedure_in.name)

    if q is not None:
        instance = q.first()
        if instance:
            return instance
    return create(db_session=db_session, procedure_in=procedure_in)


def update(
    *, db_session, procedure: Procedure, procedure_in: ProcedureUpdate
) -> Procedure:
    """Updates a procedure."""
    recipe_data = procedure.dict()

    ingredients = []
    # print(procedure_in.ingredients)
    for i in procedure_in.ingredients:
        ingredients.append(
            get_or_create_ingidient(db_session=db_session, ingredient_in=i)
        )
    steps = []
    for i in procedure_in.steps:
        steps.append(
            get_or_create_step(db_session=db_session, step_in=i)
        )

    update_data = procedure_in.dict(exclude_unset=True, exclude={"ingredients", "steps"})

    for field in recipe_data:
        if field in update_data:
            setattr(procedure, field, update_data[field])
    procedure.ingredients = ingredients
    procedure.steps = steps
    db_session.commit()
    return procedure


def delete(*, db_session, procedure_id: int):
    """Deletes a procedure."""
    procedure = db_session.query(Procedure).filter(Procedure.id == procedure_id).first()
    db_session.delete(procedure)
    db_session.commit()
