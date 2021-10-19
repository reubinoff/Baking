def test_get(session, procedure):
    from baking.routers.procedure.service import get

    t_procedure = get(db_session=session, procedure_id=procedure.id)
    import time

    assert t_procedure.id == procedure.id


def test_get_all(session, procedures):
    from baking.routers.procedure.service import get_all

    t_procedures = get_all(db_session=session).all()
    assert t_procedures
    assert len(t_procedures) == 2


def test_create(session, ingredients):
    from baking.routers.procedure.service import create
    from baking.routers.procedure.models import ProcedureCreate

    procedure_name = "procedure test"

    procedure_in = ProcedureCreate(name=procedure_name, ingredients=ingredients)

    procedure = create(db_session=session, procedure_in=procedure_in)
    assert procedure
    assert len(procedure.ingredients) == len(ingredients)
    assert procedure.ingredients[0].procedure.name == procedure_name


def test_update(session, procedure):
    from baking.routers.procedure.service import update
    from baking.routers.procedure.models import ProcedureUpdate

    name = "Updated name"

    procedure_in = ProcedureUpdate(
        name=name,
    )
    procedure = update(
        db_session=session,
        procedure=procedure,
        procedure_in=procedure_in,
    )
    assert procedure.name == name


def test_delete(session, procedure):
    from baking.routers.procedure.service import get, delete

    delete(db_session=session, procedure_id=procedure.id)
    assert not get(db_session=session, procedure_id=procedure.id)
