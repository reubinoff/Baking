# def test_create_and_update(session, cleaner, procedures, procedure):
#     from baking.routers.recipe.service import create, get
#     from baking.routers.recipe.models import RecipeCreate

#     recipe_name = "test"

#     recipe_in = RecipeCreate(name=recipe_name, procedures=procedures)

#     recipe = create(db_session=session, recipe_in=recipe_in)
#     assert recipe
#     assert len(recipe.procedures) == len(procedures)
#     assert recipe.procedures[0].recipe.name == recipe_name

#     recipe.procedures.append(procedure)
#     # print(recipe.dict())
#     recipe = get(db_session=session, recipe_id=recipe.id)
#     assert recipe
#     assert len(recipe.procedures) == len(procedures) + 1


# def test_query(session, recipe):
#     from baking.routers.recipe.service import get
#     from baking.routers.recipe.models import RecipeUpdate
#     from baking.database.services import search_filter_sort_paginate, common_parameters

#     common_parameters_in = {
#         "db_session": session,
#         "page": 1,
#         "items_per_page": 1,
#         "sort_by": [],
#         "descending": [],
#         "query_str": recipe.name
#     }
   
#     recipe_q = search_filter_sort_paginate(model="Recipe", **common_parameters_in)

#     assert recipe_q
#     assert len(recipe_q["items"]) == 1
#     assert recipe.name == recipe_q["items"][0].name

#     common_parameters_in["query_str"] = "not_found"
#     recipe_q = search_filter_sort_paginate(model="Recipe", **common_parameters_in)

#     assert recipe_q
#     assert len(recipe_q["items"]) == 0


# def test_hydration(session):
#     from baking.routers.recipe.service import create, get
#     from baking.routers.recipe.models import RecipeCreate
#     from baking.routers.procedure.models import Procedure, ProcedureCreate
#     from baking.routers.procedure.service import create as create_procedure
#     from baking.routers.ingredients.models import IngredientCreate, Ingredient
#     from baking.routers.ingredients.enums import IngrediantUnits, IngrediantType

#     ingridients = [
#         IngredientCreate(
#             name="i1_name",
#             quantity=100,
#             units=IngrediantUnits.ml,
#             type=IngrediantType.water,
#         ),
#         IngredientCreate(
#             name="i2_name",
#             quantity=200,
#             units=IngrediantUnits.ml,
#             type=IngrediantType.oil,
#         ),
#         IngredientCreate(
#             name="i3_name",
#             quantity=200,
#             units=IngrediantUnits.grams,
#             type=IngrediantType.flour,
#         ),
#     ]

#     procedure_in = ProcedureCreate(
#         name="test_procedure",
#         ingredients=ingridients,
#     )
#     procedure = create_procedure(
#         db_session=session,
#         procedure_in=procedure_in,
#     )

#     recipe_name = "test"

#     recipe_in = RecipeCreate(name=recipe_name, procedures=[procedure])
#     recipe = create(db_session=session, recipe_in=recipe_in)
#     assert recipe
#     assert recipe.hydration == 150

#     recipe.procedures[0].ingredients.append(
#         Ingredient(
#             name="i4_name",
#             quantity=200,
#             units=IngrediantUnits.grams,
#             type=IngrediantType.flour,
#         )
#     )
#     assert recipe.hydration == 75

#     p_new = Procedure(
#         name="newone",
#         ingredients=[
#             Ingredient(
#                 name="i2_name",
#                 quantity=200,
#                 units=IngrediantUnits.ml,
#                 type=IngrediantType.oil,
#             ),
#             Ingredient(
#                 name="i3_name",
#                 quantity=600,
#                 units=IngrediantUnits.grams,
#                 type=IngrediantType.flour,
#             ),
#         ],
#     )
#     recipe.procedures.append(p_new)

#     assert recipe.hydration == 50
#     assert p_new.procedure_hydration == 33


# def test_ingredients(session, cleaner):
#     from baking.routers.recipe.service import create, get
#     from baking.routers.recipe.models import RecipeCreate
#     from baking.routers.procedure.models import Procedure, ProcedureCreate
#     from baking.routers.procedure.service import create as create_procedure
#     from baking.routers.ingredients.models import IngredientCreate, Ingredient
#     from baking.routers.ingredients.enums import IngrediantUnits, IngrediantType

#     ingredients = [
#         IngredientCreate(
#             name="i1_name",
#             quantity=500,
#             units=IngrediantUnits.ml,
#             type=IngrediantType.water,
#         ),
#         IngredientCreate(
#             name="i2_name",
#             quantity=50,
#             units=IngrediantUnits.ml,
#             type=IngrediantType.oil,
#         ),
#         IngredientCreate(
#             name="i3_name",
#             quantity=200,
#             units=IngrediantUnits.grams,
#             type=IngrediantType.flour,
#         ),
#         IngredientCreate(
#             name="i4_name",
#             quantity=300,
#             units=IngrediantUnits.grams,
#             type=IngrediantType.flour,
#         ),
#     ]

#     procedure_in_a = ProcedureCreate(
#         name="test_procedure",
#         ingredients=[IngredientCreate(
#             name="i3_name",
#             quantity=200,
#             units=IngrediantUnits.grams,
#             type=IngrediantType.flour,
#         )],
#     )
#     procedure_in_b = ProcedureCreate(
#         name="test_procedure",
#         ingredients=ingredients,
#     )
#     procedure_a = create_procedure(
#         db_session=session,
#         procedure_in=procedure_in_a,
#     )
#     procedure_b = create_procedure(
#         db_session=session,
#         procedure_in=procedure_in_b,
#     )

#     recipe_name = "test"

#     recipe_in = RecipeCreate(name=recipe_name, procedures=[
#                              procedure_a, procedure_b])
#     recipe = create(db_session=session, recipe_in=recipe_in)
#     assert recipe

#     r = get(db_session=session, recipe_id=recipe.id)
#     for i in r.ingredients:
#         if i.name == "i3_name":
#             assert i.quantity == 400
#             assert i.units == IngrediantUnits.grams
#             assert i.type == IngrediantType.flour
#             assert i.precentage == 0.57

        
