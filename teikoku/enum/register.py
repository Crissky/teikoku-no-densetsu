from enum import Enum


class PlayerAttrEnum(Enum):
    USER_ID = "user_id"
    NAME = "name"
    USERNAME = "username"
    SILENT = "silent"
    ALLOW_PRIVATE_MESSAGES = "allow_private_messages"


class GroupAttrEnum(Enum):
    CHAT_ID = "chat_id"
    NAME = "name"
    SILENT = "silent"
