from enum import Enum


class PopulateFieldEnum(Enum):
    CALLBACK = "factory"
    INITIATOR = "initiator"


class SaveFieldEnum(Enum):
    ATTRIBUTES = "attributes"
