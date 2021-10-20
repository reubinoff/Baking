from enum import Enum


class IngrediantUnits(str, Enum):
    """Grams for sold and ml for liquieds"""

    grams = "Grams"
    ml = "MilliLiter"

    def __str__(self) -> str:
        return str.__str__(self)


class IngrediantType(str, Enum):
    water = "Water"
    flour = "Flour"
    salt = "Salt"
    oil = "Oil"
    yeast = "Yeast"

    Other = "Other"

    def __str__(self) -> str:
        return str.__str__(self)


class IngrediantTypeState(Enum):
    liquid = 0
    solid = 1


convertion_table = {
    IngrediantType.water: IngrediantTypeState.liquid,
    IngrediantType.flour: IngrediantTypeState.solid,
    IngrediantType.salt: IngrediantTypeState.solid,
    IngrediantType.oil: IngrediantTypeState.liquid,
    IngrediantType.yeast: IngrediantTypeState.solid,
}


def is_liquid(ingridiant_type: IngrediantType) -> bool:
    state = convertion_table.get(ingridiant_type, IngrediantTypeState.solid)
    return state == IngrediantTypeState.liquid
