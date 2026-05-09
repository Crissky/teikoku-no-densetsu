from telegram import Update
from telegram.ext import ContextTypes, PrefixHandler, CommandHandler

from bot.constants.commands import SIGNUP_COMMNADS
from bot.constants.filters import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.constants.sections import PLAYER_SUBSECTION_NAME, SIGNUP_SECTION_NAME
from bot.functions.messages import reply_message
from bot.functions.user import get_username
from general.functions.text import create_text_in_box, format_subsection
from repository.mongo.functions.player import exists_player, save_player
from teikoku.player import Player


async def signup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    full_name = update.effective_user.full_name
    username = get_username(update=update)
    player = Player(user_id=user_id, name=full_name, username=username)

    if exists_player(player.user_id):
        reply_text = (
            f"Player com USER ID: '{player.user_id}', já está cadastrado."
        )
    else:
        new_player = save_player(player)
        player_telegram_text = new_player.telegram_text
        subsection = format_subsection(text=PLAYER_SUBSECTION_NAME)
        reply_text = (
            f"Olá {username or full_name}!\n"
            f"Você foi cadastrado com sucesso!\n\n"
            f"{subsection}"
            f"{player_telegram_text}"
        )

    reply_text = create_text_in_box(
        text=reply_text, section_name=SIGNUP_SECTION_NAME
    )
    await reply_message(
        function_caller="SIGNUP()",
        text=reply_text,
        context=context,
        update=update,
        markdown=True,
    )


SIGNUP_HANDLERS = [
    PrefixHandler(
        PREFIX_COMMANDS, SIGNUP_COMMNADS, signup, BASIC_COMMAND_FILTER
    ),
    CommandHandler(SIGNUP_COMMNADS, signup, BASIC_COMMAND_FILTER),
]
