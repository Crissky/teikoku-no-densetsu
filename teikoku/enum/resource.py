from enum import Enum


class ResourceEnum(Enum):
    CULTURE = "cultura"
    FAITH = "fé"
    FOOD = "alimento"
    METAL = "metal"
    PRECIOUS_METAL = "metal precioso"
    SCIENCE = "ciência"
    STONE = "rocha"
    WOOD = "madeira"


class LocationResourceTypeEnum(Enum):
    MINE = "mina"
    DEPOSIT = "JAZIDA"
    FOREST = "floresta"
    TEMPLE = "templo"
