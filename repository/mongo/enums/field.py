from enum import Enum


class PopulateFieldEnum(Enum):
    CLASS = "class"
    FACTORY = "factory"
    MODEL = "model"
    OVERCLASS = "overclass"


class SaveFieldEnum(Enum):
    ATTRIBUTES = "attributes"
