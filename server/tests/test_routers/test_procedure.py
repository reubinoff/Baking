def test_get(session, cleaner, procedure):
    from baking.routers.procedure.service import get

    t_procedure = get(db_session=session, procedure_id=procedure.id)
    import time

    assert t_procedure.id == procedure.id


def test_get_all(session, procedures):
    from baking.routers.procedure.service import get_all

    t_procedures = get_all(db_session=session).all()
    assert t_procedures


def test_create(session, ingredients, steps):
    from baking.routers.procedure.service import create
    from baking.routers.procedure.models import ProcedureCreate

    procedure_name = "procedure test"

    procedure_in = ProcedureCreate(
        name=procedure_name, ingredients=ingredients, steps=steps)

    procedure = create(db_session=session, procedure_in=procedure_in)
    assert procedure
    assert len(procedure.ingredients) == len(ingredients)
    assert procedure.ingredients[0].procedure.name == procedure_name


def test_update(session, procedure, steps):
    from baking.routers.procedure.service import update
    from baking.routers.procedure.models import ProcedureUpdate

    name = "Updated name"
    step_steps = len(procedure.steps)
    procedure_in = ProcedureUpdate(
        name=name,
        steps=procedure.steps
    )
    procedure_in.steps.extend(steps)
    procedure = update(
        db_session=session,
        procedure=procedure,
        procedure_in=procedure_in,
    )
    assert procedure.name == name
    assert len(procedure.steps) == len(steps) + step_steps


def test_delete(session, procedure):
    from baking.routers.procedure.service import get, delete

    delete(db_session=session, procedure_id=procedure.id)
    assert not get(db_session=session, procedure_id=procedure.id)
