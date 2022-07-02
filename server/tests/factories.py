from baking.routers.procedure.models import Procedure
from faker import Faker

from factory import Sequence, post_generation, SubFactory, LazyAttribute, List, RelatedFactory, RelatedFactoryList
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyChoice, FuzzyText, FuzzyDateTime, FuzzyInteger


from baking.routers.recipe.models import Recipe
from baking.routers.ingredients.models import Ingredient
from baking.routers.steps.models import Step
from baking.routers.ingredients.enums import IngrediantType, IngrediantUnits


from .database import Session


class BaseFactory(SQLAlchemyModelFactory):
    """Base Factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = "commit"


class RecipeFactory(BaseFactory):
    """Recipe Factory."""

    name = Sequence(lambda n: f"recipe_{n}")
    description = Sequence(lambda n: f"blaBla_{n}")

    class Meta:
        """Factory Configuration."""

        model = Recipe


class IngredientFactory(BaseFactory):
    """Ingredient Factory."""

    name = Sequence(lambda n: f"ingredient_{n}")
    quantity = FuzzyInteger(1, 1000)
    units = FuzzyChoice(list(map(str, IngrediantUnits)))
    type = FuzzyChoice(list(map(str, IngrediantType)))

    procedure = SubFactory(
        'tests.factories.ProcedureFactory', ingredients=None)

    class Meta:
        """Factory Configuration."""

        model = Ingredient


class StepFactory(BaseFactory):
    """Ingredient Factory."""

    name = Sequence(lambda n: f"step_{n}")
    description = Sequence(lambda n: f"step_{n}")
    duration_in_seconds = FuzzyInteger(1, 10000)

    procedure = SubFactory(
        'tests.factories.ProcedureFactory', steps=None)

    class Meta:
        """Factory Configuration."""

        model = Step

class ProcedureFactory(BaseFactory):
    """Ingredient Factory."""

    name = Sequence(lambda n: f"procedure_{n}")
    description = Sequence(lambda n: f"blaBla_{n}")
    order = FuzzyInteger(1, 10)

    ingredients = RelatedFactoryList(
        IngredientFactory, size=3, factory_related_name="procedure")
    steps = RelatedFactoryList(
        StepFactory, size=3, factory_related_name="procedure")

    class Meta:
        """Factory Configuration."""

        model = Procedure
        
