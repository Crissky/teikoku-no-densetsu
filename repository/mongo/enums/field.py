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
    GROUP = "effective_chat.id"
    PLAYER = "effective_user.id"
    WORLD = "effective_chat.id"
    CITY = "effective_chat.id"


class ContextAltIdEnum(Enum):
    GROUP = "_chat_id"
    PLAYER = "_user_id"
    WORLD = "_chat_id"
    CITY = "_chat_id"
