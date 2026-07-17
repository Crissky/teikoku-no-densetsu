from enum import Enum


class PopulateFieldEnum(Enum):
    CALLBACK = "factory"
    INITIATOR = "initiator"


class SaveFieldEnum(Enum):
    ATTRIBUTES = "attributes"


class AltIdEnum(Enum):
    GROUP = "chat_id"
    PLAYER = "user_id"
    WORLD = "chat_id"
    CITY = "owner"
