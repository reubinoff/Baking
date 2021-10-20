from baking.routers.procedure.models import Procedure
from faker import Faker

from factory import Sequence, post_generation, SubFactory, LazyAttribute
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyChoice, FuzzyText, FuzzyDateTime, FuzzyInteger


from baking.routers.recipe.models import Recipe
from baking.routers.ingredients.models import Ingredient
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

    # @post_generation
    # def ingredients(self, create, extracted, **kwargs):
    #     if not create:
    #         return

    #     if extracted:
    #         for ingredients in extracted:
    #             self.ingredients.append(ingredients)

    # @post_generation
    # def procedures(self, create, extracted, **kwargs):
    #     if not create:
    #         return

    #     if extracted:
    #         for procedures in extracted:
    #             self.procedures.append(procedures)


class IngredientFactory(BaseFactory):
    """Ingredient Factory."""

    name = Sequence(lambda n: f"ingredient_{n}")
    quantity = FuzzyInteger(1, 1000)
    units = FuzzyChoice(list(map(str, IngrediantUnits)))
    type = FuzzyChoice(list(map(str, IngrediantType)))

    class Meta:
        """Factory Configuration."""

        model = Ingredient


class ProcedureFactory(BaseFactory):
    """Ingredient Factory."""

    name = Sequence(lambda n: f"procedure_{n}")
    description = Sequence(lambda n: f"blaBla_{n}")
    order = FuzzyInteger(1, 10)

    class Meta:
        """Factory Configuration."""

        model = Procedure
