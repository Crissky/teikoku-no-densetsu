from telegram import Update
from telegram.ext import (
    ContextTypes,
    PrefixHandler,
    CommandHandler,
)

from bot.constants.command import (
    SIGNUP_COMMANDS,
)
from bot.constants.filter import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.constants.message import (
    PLAYER_ALREADY_REGISTERED_ERROR,
    PLAYER_SUCCESSFULLY_REGISTERED_FORMAT,
)
from bot.constants.section import (
    FAIL_SIGNUP_SECTION_NAME,
    PLAYER_SUBSECTION_NAME,
    SIGNUP_SECTION_NAME,
)
from bot.functions.message import (
    MIN_AUTODELETE_TIME,
    reply_message,
)
from bot.functions.user import get_username
from general.functions.text import create_text_in_box, format_subsection
from repository.mongo.functions.player import (
    exists_player,
    save_player,
)
from teikoku.entity.register.player import Player


async def signup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cadastro do player."""

    user_id = update.effective_user.id
    full_name = update.effective_user.full_name
    username = get_username(update=update)
    player = Player(user_id=user_id, name=full_name, username=username)

    if exists_player(player.user_id):  # JÁ CADASTRADO
        section_name = FAIL_SIGNUP_SECTION_NAME
        reply_text = PLAYER_ALREADY_REGISTERED_ERROR.format(id=player.user_id)
    else:  # CADASTRO
        section_name = SIGNUP_SECTION_NAME
        new_player = save_player(player)
        player_telegram_text = new_player.telegram_text
        subsection = format_subsection(text=PLAYER_SUBSECTION_NAME)
        reply_text = PLAYER_SUCCESSFULLY_REGISTERED_FORMAT.format(
            name=(username or full_name),
            subsection=subsection,
            telegram_text=player_telegram_text,
        )

    reply_text = create_text_in_box(text=reply_text, section_name=section_name)
    await reply_message(
        function_caller="SIGNUP()",
        text=reply_text,
        context=context,
        update=update,
        markdown=True,
        auto_delete_message=MIN_AUTODELETE_TIME,
    )


SIGNUP_PLAYER_HANDLERS = [
    # SIGNUP
    PrefixHandler(
        PREFIX_COMMANDS, SIGNUP_COMMANDS, signup, BASIC_COMMAND_FILTER
    ),
    CommandHandler(SIGNUP_COMMANDS, signup, BASIC_COMMAND_FILTER),
]
