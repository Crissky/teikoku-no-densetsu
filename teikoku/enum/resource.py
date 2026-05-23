from enum import Enum


class CollectibleResourceEnum(Enum):
    FOOD = "alimento"
    METAL = "metal"
    PRECIOUS_METAL = "metal precioso"
    STONE = "rocha"
    WOOD = "madeira"


class SocialResourceEnum(Enum):
    CULTURE = "cultura"
    FAITH = "fé"
    SCIENCE = "ciência"


ResourceEnum = Enum(
    "ResourceEnum",
    {**CollectibleResourceEnum.__members__, **SocialResourceEnum.__members__},
)


class LocationResourceTypeEnum(Enum):
    MINE = "mina"
    DEPOSIT = "jazida"
    FOREST = "floresta"
    TEMPLE = "templo"


print(CollectibleResourceEnum, list(CollectibleResourceEnum), end="\n\n")
print(SocialResourceEnum, list(SocialResourceEnum), end="\n\n")
print(ResourceEnum, list(ResourceEnum), end="\n\n")
print(type(ResourceEnum.METAL), end="\n\n")
