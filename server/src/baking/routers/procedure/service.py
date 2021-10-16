from typing import Optional, List

from .models import ProcedureRead, ProcedureCreate, Procedure


def get(*, db_session, procedure_id: int) -> Optional[Procedure]:
    """Returns a item based on the given Procedure id."""
    return (
        db_session.query(Procedure).filter(Procedure.id == procedure_id).one_or_none()
    )


def get_all(*, db_session) -> List[Optional[Procedure]]:
    """Returns all Procedures."""
    return db_session.query(Procedure)


def create(*, db_session, procedure_in: ProcedureCreate) -> Procedure:
    """Creates a new Procedure."""
    procedure = Procedure(**procedure_in.dict())

    db_session.add(procedure)
    db_session.commit()
    return procedure
