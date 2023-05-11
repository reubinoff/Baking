from enum import Enum


class IngredientUnits(str, Enum):
    """Grams for sold and ml for liquieds"""

    grams = "Grams"
    ml = "MilliLiter"

    def __str__(self) -> str:
        return str.__str__(self)


class IngredientType(str, Enum):
    water = "Water"
    flour = "Flour"
    salt = "Salt"
    oil = "Oil"
    yeast = "Yeast"

    Other = "Other"

    def __str__(self) -> str:
        return str.__str__(self)


class IngredientTypeState(Enum):
    liquid = 0
    solid = 1


convertion_table = {
    IngredientType.water: IngredientTypeState.liquid,
    IngredientType.flour: IngredientTypeState.solid,
    IngredientType.salt: IngredientTypeState.solid,
    IngredientType.oil: IngredientTypeState.liquid,
    IngredientType.yeast: IngredientTypeState.solid,
}


def is_type_liquid(ingridiant_type: IngredientType) -> bool:
    state = convertion_table.get(ingridiant_type, IngredientTypeState.solid)
    return state == IngredientTypeState.liquid
