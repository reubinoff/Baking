from faker import Faker

from factory import Sequence, post_generation, SubFactory, LazyAttribute
from factory.alchemy import SQLAlchemyModelFactory


from baking.routers.recipe.models import Recipe


from .database import Session


class BaseFactory(SQLAlchemyModelFactory):
    """Base Factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = "commit"


class RecipeFactory(BaseFactory):
    """Participant Factory."""

    name = Sequence(lambda n: f"recipe_{n}")
    description = Sequence(lambda n: f"blaBla_{n}")

    class Meta:
        """Factory Configuration."""

        model = Recipe

    @post_generation
    def ingredients(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for ingredients in extracted:
                self.ingredients.append(ingredients)

    @post_generation
    def procedures(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for procedures in extracted:
                self.procedures.append(procedures)
