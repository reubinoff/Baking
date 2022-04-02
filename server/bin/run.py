import imp
import logging
from re import I
import random
import uvicorn
import os

from alembic import command as alembic_command
from alembic.config import Config as AlembicConfig
from sqlalchemy.orm import scoped_session, sessionmaker

from src.baking.config import settings
from src.baking.database.manage import internal_create_database_for_tests
from src.baking.database.core import engine
from baking.database.manage import init_database

import requests

word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

response = requests.get(word_site)
WORDS = response.content.splitlines()
TOTAL_RECIPES = 50


Session = scoped_session(sessionmaker())

def db():
    init_database(engine)

    session = sessionmaker(bind=engine)
    return session()

def get_words(num_of_words):
    return ' '.join([WORDS[random.randint(0, len(WORDS)-1)].decode() for i in range(num_of_words)])

def load_db():
    session = db()
    from baking.routers.ingredients.models import Ingredient
    from baking.routers.procedure.models import Procedure
    from baking.routers.recipe.models import Recipe
    from baking.routers.ingredients.enums import IngrediantUnits, IngrediantType
    TYPES = list(map(str, IngrediantType))
    session.query(Ingredient).delete()
    session.query(Procedure).delete()
    session.query(Recipe).delete()
    for i in range(1, TOTAL_RECIPES):
        p = []
        for j in range(1, random.randint(2, 5)):
            ingredients = []
            for k in range(1, random.randint(2, 7)):
                type = TYPES[random.randint(0, len(TYPES)-1)]
                ingredients.append(Ingredient(name=f"i_{get_words(random.randint(1,3))}_{k}", type=type, quantity=random.randint(1,1000), units="Grams"))
            p.append( Procedure(name=f"procedure_{i}_{j}", order=j, ingredients=ingredients, description=get_words(random.randint(1,10))))
        aaa = Recipe(name=f"{get_words(2)} {i}", description=get_words(10), procedures=p)
        session.add(aaa)

    session.commit()
    session.close()

if __name__ == "__main__":
    internal_create_database_for_tests(engine=engine)
    revision = "head" 
    alembic_cfg = AlembicConfig(settings.alembix_ini)
    alembic_cfg.set_main_option("script_location", settings.revisions_location)
    alembic_command.upgrade(alembic_cfg, revision)
    print("Migration ended")
    # load_db()

    uvicorn.run(
        "src.baking.main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8888")),
        log_level=logging.DEBUG,
    )


