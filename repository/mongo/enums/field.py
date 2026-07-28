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


class UpdateAltIdEnum(Enum):
    GROUP = "effective_chat"
    PLAYER = "effective_user"
    WORLD = "effective_chat"
    CITY = "effective_chat"


class ContextAltIdEnum(Enum):
    GROUP = "_chat_id"
    PLAYER = "_user_id"
    WORLD = "_chat_id"
    CITY = "_chat_id"
