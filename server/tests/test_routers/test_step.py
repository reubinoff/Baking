
# def test_get(session, cleaner, step):
#     from baking.routers.steps.service import get

#     t_ingredient = get(db_session=session, step_id=step.id)
#     assert t_ingredient.id == step.id


# def test_get_all(session, steps):
#     from baking.routers.steps.service import get_all
#     procedure_id = steps[0].procedure.id
#     t_steps = get_all(
#         db_session=session, procedure_id=procedure_id)
#     assert t_steps
#     assert len(t_steps) == len(
#         [i for i in steps if i.procedure.id == procedure_id])


# def test_create(session, procedure):
#     from baking.routers.steps.service import create
#     from baking.routers.steps.models import StepCreate

#     step_in = StepCreate(
#         name="teststs",
#         description="test",
#         duration_in_seconds=234,
#         procedure_id=procedure.id
#     )
#     # print(recipe_in.dict())
#     steps = create(db_session=session, step_in=step_in)
#     assert steps


# def test_update(session, step):
#     from baking.routers.steps.service import update
#     from baking.routers.steps.models import StepUpdate

#     name = "Updated name"

#     step_in = StepUpdate(
#         name=name,
#     )
#     recipe = update(
#         db_session=session,
#         step=step,
#         step_in=step_in,
#     )
#     assert step.name == name


# def test_delete(session, step):
#     from baking.routers.steps.service import get, delete

#     delete(db_session=session, step_id=step.id)
#     assert not get(db_session=session, step_id=step.id)
