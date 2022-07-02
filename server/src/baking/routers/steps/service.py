from asyncio.log import logger
import logging
from typing import Optional, List
from .models import StepBase, StepRead, StepCreate, StepUpdate, Step

LOGGER = logging.getLogger(__name__)

def get(*, db_session,step_id: int) -> Optional[Step]:
    """Returns a step based on the given step id."""
    return (
        db_session.query(Step)
        .filter(Step.id == step_id)
        .one_or_none()
    )


def get_all(*, db_session, procedure_id: int) -> List[Optional[Step]]:
    """Returns all steps for given procedure."""
    return db_session.query(Step).filter(Step.procedure_id == procedure_id).all()


def create(*, db_session, step_in: StepCreate) -> Step:
    """Creates a new step."""
    step = Step(**step_in.dict())

    db_session.add(step)
    db_session.commit()
    return step


def get_or_create(*, db_session, step_in: StepCreate) -> Step:
    """Gets or creates a new step."""
    q = None
    if step_in.id:
        q = db_session.query(Step).filter(Step.id == step_in.id)

    if q is not None:
        instance = q.first()
        if instance:
            return instance
    return create(db_session=db_session, step_in=step_in)


def delete(*, db_session, step_id: int):
    """Deletes a step."""
    try:
        step = (
            db_session.query(Step).filter(Step.id == step_id).first()
        )
    except Exception:
        logger.warning(f"Failed to delete step {step_id}")
        return
    db_session.delete(step)
    db_session.commit()


def update(
    *, db_session, step: Step, step_in: StepUpdate
) -> Step:
    """Updates a step."""
    step_data = step.dict()

    update_data = step_in.dict(exclude_unset=True, exclude={})

    for field in step_data:
        if field in update_data:
            setattr(step, field, update_data[field])

    db_session.commit()
    return step
