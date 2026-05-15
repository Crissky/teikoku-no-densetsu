import re

# CALLBACK COMMANDS ==========================================================
CALLBACK_COMMAND_CLOSE = "$close"

# PLAYER
CALLBACK_COMMAND_REFRESH_PLAYER = "$refresh_player"
CALLBACK_COMMAND_UPDATE_PLAYER = "$update_player"

# GROUP
CALLBACK_COMMAND_REFRESH_GROUP = "$refresh_group"
CALLBACK_COMMAND_UPDATE_GROUP = "$update_group"

ESCAPED_CALLBACK_COMMAND_CLOSE = re.escape(CALLBACK_COMMAND_CLOSE)
