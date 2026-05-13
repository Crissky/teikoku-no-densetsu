from telegram import MessageEntity
from telegram.ext import filters


PREFIX_COMMANDS = ["!", "p!"]
BASIC_COMMAND_FILTER = (
    ~filters.FORWARDED
    & ~filters.UpdateType.EDITED
    & ~filters.Entity(MessageEntity.URL)
    & ~filters.Entity(MessageEntity.TEXT_LINK)
)
BASIC_COMMAND_IN_GROUP_FILTER = filters.ChatType.GROUPS & BASIC_COMMAND_FILTER
ALLOW_WRITE_TEXT_ONLY_IN_GROUP_FILTER = (
    filters.TEXT
    & filters.ChatType.GROUPS
    & ~filters.COMMAND
    & ~filters.FORWARDED
    & ~filters.UpdateType.EDITED
    & ~filters.Regex(f'^[{"".join(PREFIX_COMMANDS)}]')
)
ALLOW_GAIN_XP_FILTER = (
    filters.ChatType.GROUPS
    & ~filters.COMMAND
    & ~filters.FORWARDED
    & ~filters.UpdateType.EDITED
    & ~filters.Regex(f'^[{"".join(PREFIX_COMMANDS)}]')
)
