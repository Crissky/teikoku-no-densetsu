from enum import Enum


class ContextKeyEnum(Enum):
    GROUP = "group"
    PLAYER = "player"


class ContextDataTypeEnum(Enum):
    BOT = "bot"
    CHAT = "chat"
    USER = "user"
