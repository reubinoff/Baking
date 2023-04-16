
async def test_create_and_update(database, procedures, procedure):
    from baking.routers.recipe.service import create, get, update
    from baking.routers.recipe.models import RecipeCreate, RecipeUpdate

    recipe_name = "test"

    recipe_in = RecipeCreate(name=recipe_name, procedures=procedures)

    recipe = await create(db=database, recipe_in=recipe_in)
    assert recipe
    assert len(recipe.procedures) == len(procedures)
    assert recipe.name == recipe_name

    procedures.append(procedure)
    
    recipe_in = RecipeUpdate(
        procedures=procedures
    )
    t_recipe = await update(
        db=database,
        recipe_id=recipe.id,
        recipe_in=recipe_in,
    )

    t_recipe = await get(db=database, recipe_id=recipe.id)
    assert t_recipe
    assert len(t_recipe.procedures) == len(procedures)
    assert t_recipe.name == recipe_name



async def test_hydration(database):
    from baking.routers.recipe.service import create, get, update
    from baking.routers.recipe.models import RecipeCreate, RecipeUpdate
    from baking.routers.procedure.models import ProcedureUpdate, ProcedureCreate
    from baking.routers.ingredients.models import IngredientCreate, Ingredient
    from baking.routers.ingredients.enums import IngrediantUnits, IngrediantType

    ingredients = [
        IngredientCreate(
            name="i1_name",
            quantity=100,
            units=IngrediantUnits.ml,
            type=IngrediantType.water,
        ),
        IngredientCreate(
            name="i2_name",
            quantity=200,
            units=IngrediantUnits.ml,
            type=IngrediantType.oil,
        ),
        IngredientCreate(
            name="i3_name",
            quantity=200,
            units=IngrediantUnits.grams,
            type=IngrediantType.flour,
        ),
    ]

    procedure_in = ProcedureCreate(
        name="test_procedure",
        ingredients=ingredients,
    )

    recipe_name = "test"

    recipe_in = RecipeCreate(name=recipe_name, procedures=[procedure_in])
    recipe = await create(db=database, recipe_in=recipe_in)
    assert recipe
    assert recipe.hydration == 150

    recipe.procedures[0].ingredients.append(
        Ingredient(
            name="i4_name",
            quantity=200,
            units=IngrediantUnits.grams,
            type=IngrediantType.flour,
        )
    )
    r = RecipeUpdate(
        procedures=recipe.procedures
    )
    recipe = await update(
        db=database,
        recipe_id=recipe.id,
        recipe_in=r,
    )
    t_r = await get(db=database, recipe_id=recipe.id)

    assert t_r.hydration == 75

    recipe.procedures.append( ProcedureCreate(
        name="newone",
        ingredients=[
            Ingredient(
                name="i2_name",
                quantity=200,
                units=IngrediantUnits.ml,
                type=IngrediantType.oil,
            ),
            Ingredient(
                name="i3_name",
                quantity=600,
                units=IngrediantUnits.grams,
                type=IngrediantType.flour,
            ),
        ],
    ))
    r = RecipeUpdate(
        procedures=recipe.procedures
    )
    recipe = await update(
        db=database,
        recipe_id=recipe.id,
        recipe_in=r,
    )
    t_r = await get(db=database, recipe_id=recipe.id)
    assert len(t_r.procedures) == 2
    assert t_r.hydration == 50
    assert t_r.procedures[1].procedure_hydration == 33

async def test_ingredients(database):
    from baking.routers.recipe.service import create, get, update
    from baking.routers.recipe.models import RecipeCreate, RecipeUpdate
    from baking.routers.procedure.models import ProcedureCreate
    from baking.routers.ingredients.models import IngredientCreate
    from baking.routers.ingredients.enums import IngrediantUnits, IngrediantType

    ingredients = [
        IngredientCreate(
            name="i1_name",
            quantity=500,
            units=IngrediantUnits.ml,
            type=IngrediantType.water,
        ),
        IngredientCreate(
            name="i2_name",
            quantity=50,
            units=IngrediantUnits.ml,
            type=IngrediantType.oil,
        ),
        IngredientCreate(
            name="i3_name",
            quantity=200,
            units=IngrediantUnits.grams,
            type=IngrediantType.flour,
        ),
        IngredientCreate(
            name="i4_name",
            quantity=300,
            units=IngrediantUnits.grams,
            type=IngrediantType.flour,
        ),
    ]

    procedure_in_a = ProcedureCreate(
        name="test_procedure",
        ingredients=[IngredientCreate(
            name="i3_name",
            quantity=200,
            units=IngrediantUnits.grams,
            type=IngrediantType.flour,
        )],
    )
    procedure_in_b = ProcedureCreate(
        name="test_procedure",
        ingredients=ingredients,
    )

    recipe_name = "test"

    recipe_in = RecipeCreate(name=recipe_name, procedures=[
                             procedure_in_a, procedure_in_b])
    recipe = await create(db=database, recipe_in=recipe_in)
    assert recipe

    r = await get(db=database, recipe_id=recipe.id)
    assert r.total_liquid == 550
    assert r.total_solid == 700
    for i in r.ingredients:
        if i.name == "i3_name":
            assert i.quantity == 400
            assert i.units == IngrediantUnits.grams
            assert i.type == IngrediantType.flour
            assert i.precentage == 0.57

    # add ingredients to procedure
    procedure_in_c = ProcedureCreate(
        name="test_procedure",
        ingredients=[IngredientCreate(
            name="i3_name",
            quantity=200,
            units=IngrediantUnits.grams,
            type=IngrediantType.flour,
        )],
    )
    r.procedures.append(procedure_in_c)
    r = RecipeUpdate(
        procedures=r.procedures
    )
    recipe = await update(
        db=database,
        recipe_id=recipe.id,
        recipe_in=r,
    )
    t_r = await get(db=database, recipe_id=recipe.id)
    assert len(t_r.procedures) == 3
    assert t_r.total_liquid == 550
    assert t_r.total_solid == 900
    for i in t_r.ingredients:
        if i.name == "i3_name":
            assert i.quantity == 600
            assert i.units == IngrediantUnits.grams
            assert i.type == IngrediantType.flour
            assert i.precentage == 0.67

async def test_total_recipe_time(database, recipe_factory, steps, procedure):
    recipe = await recipe_factory.create_async()

    total_recipe_time = 0
    for p in recipe.procedures:
        for s in p.steps:
            total_recipe_time += s.duration_in_seconds
    print(total_recipe_time)
    assert recipe.total_recipe_time == total_recipe_time
