from typing import Optional, List

from baking.models import FileUploadData
from baking.routers.ingredients.enums import is_liquid

from baking.routers.recipe.models import RecipeRead, Recipe, RecipeCreate, RecipeUpdate

from baking.routers.procedure.service import get_or_create as get_or_create_procedure
from baking.routers.ingredients.models import IngredientRead


def get(*, db_session, recipe_id: int) -> Optional[Recipe]:
    """Returns a recipe based on the given recipe id."""
    recipe = db_session.query(Recipe).filter(Recipe.id == recipe_id).one_or_none()
    if recipe is None:
        return None
    recipe.ingredients = _get_ingridients(recipe=recipe)
    return recipe

def _calculate_precentage(*, ingredients: List[IngredientRead]) -> List[IngredientRead]:
    """Returns a recipe based on the given recipe id."""
    total_liquid = 0
    total_solid = 0
    for ingredient in ingredients:
        if is_liquid(ingredient.type):
            total_liquid += ingredient.quantity # TODO: need to cover if the units are different
        else:
            total_solid += ingredient.quantity
    

def _get_ingridients(*, recipe: Recipe) -> List[Optional[IngredientRead]]:
    """Returns a ingridients list"""
    total_liquid = 0
    total_solid = 0
    max_precentage_liquid: float = recipe.hydration/100
    ingredients = dict()
    if recipe.procedures is not None:
        for p in recipe.procedures:
            for i in p.ingredients:
                if i.name in ingredients:
                    ingredients[i.name].quantity = ingredients[i.name].quantity + i.quantity
                else:
                    ingredients[i.name] = IngredientRead(**i.dict())
                if is_liquid(i.type):
                    total_liquid += i.quantity ## TODO: need to cover if the units are different
                else:
                    total_solid += i.quantity

    for name, ingredient in ingredients.items():
        if is_liquid(ingredient.type):
            ingredient.precentage = round(
                (ingredient.quantity / total_liquid) * max_precentage_liquid, 2)
        else:
            ingredient.precentage = round(
                (ingredient.quantity / total_solid) , 2)

    return list(ingredients.values())

def get_all(*, db_session) -> List[Optional[Recipe]]:
    """Returns all recipes."""
    return db_session.query(Recipe)


def create(*, db_session, recipe_in: RecipeCreate) -> Recipe:
    """Creates a new Recipe."""
    if db_session is None:
        return None
    procedures = []
    if recipe_in.procedures is not None and isinstance(recipe_in.procedures, List):
        procedures = [
            get_or_create_procedure(db_session=db_session, procedure_in=procedure_in)
            for procedure_in in recipe_in.procedures
        ]

    recipe = Recipe(**recipe_in.dict(exclude={"procedures"}), procedures=procedures)
    # print(recipe_in.dict())
    db_session.add(recipe)
    db_session.commit()
    return recipe


def update(*, db_session, recipe: Recipe, recipe_in: RecipeUpdate) -> Recipe:
    """Updates a recipe."""
    recipe_data = recipe.dict()

    procedures = []
    # print(recipe_in.procedures)
    for p in recipe_in.procedures:
        procedures.append(
            get_or_create_procedure(db_session=db_session, procedure_in=p)
        )

    update_data = recipe_in.dict(exclude_unset=True, exclude={"procedures"})

    for field in recipe_data:
        if field in update_data:
            setattr(recipe, field, update_data[field])
    recipe.procedures = procedures

    db_session.commit()
    return recipe


def update_image(*, db_session, recipe: Recipe, image: FileUploadData):
    """Updates a recipe."""
    recipe.image_url = image.url
    recipe.image_identidier = image.identidier

    db_session.commit()
    return recipe

def delete(*, db_session, recipe_id: int):
    """Deletes a recipe."""
    recipe = db_session.query(Recipe).filter(Recipe.id == recipe_id).first()
    db_session.delete(recipe)
    db_session.commit()


if __name__ == "__main__":
    from baking.routers.procedure.models import ProcedureRead
    from baking.routers.ingredients.models import IngredientRead
    from baking.routers.ingredients.enums import IngrediantType, IngrediantUnits

    i1 = IngredientRead(name="flour_a", quantity=400, procedure_id=5, id=5,
                          type=IngrediantType.flour, units=IngrediantUnits.grams)
    i2 = IngredientRead(name="flour_b", quantity=300, units=IngrediantUnits.grams, procedure_id=5, id=1,
                          type=IngrediantType.flour)
    i3 = IngredientRead(name="water", quantity=500, units=IngrediantUnits.grams, procedure_id=5, id=2,
                          type=IngrediantType.water)
    i4 = IngredientRead(name="oil", quantity=50, procedure_id=5, id=3,
                        type=IngrediantType.oil, units=IngrediantUnits.grams)
    ingredients = [i1, i2, i3, i4]
    p = ProcedureRead(name="test", description="test", ingredients=ingredients , id=5, order=1, recipe_id=1, procedure_hydration=71, duration_in_seconds=60)
    recipe = RecipeRead(name="test", description="test", procedures=[
                        p], hydration=round((550/700)*100, 2), id=1)
    rec = RecipeRead(**recipe.dict())
    l = _get_ingridients(recipe=recipe)
    print(recipe.dict())