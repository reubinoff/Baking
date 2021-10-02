from enum import Enum


class Units(str, Enum):
    grams = "Grams"
    liter = "Liter"
    ml = "MilliLiter"

    def __str__(self) -> str:
        return str.__str__(self)

class IngrediantType(str, Enum):
    water = "Water"
    flour = "Flour"
    salt = "Salt"

    Other = "Other"

    def __str__(self) -> str:
        return str.__str__(self)