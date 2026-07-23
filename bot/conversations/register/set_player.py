from bot.constants.command import SET_ATTR_PLAYER_COMMANDS
from bot.constants.filter import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.constants.message import (
    FAIL_UPDATE_NOT_ARGS_FORMAT,
    NO_CHANGE_IN_PLAYER_MSG,
)
from bot.constants.section import (
    FAIL_UPDATE_PLAYER_SECTION_NAME,
    PLAYER_SUBSECTION_NAME,
    UPDATE_PLAYER_SECTION_NAME,
)
from bot.decorators.player import need_signedup_player
from bot.functions.arg import format_args
from bot.functions.message import MIN_AUTODELETE_TIME, reply_message
from general.functions.text import create_text_in_box, format_subsection
from repository.mongo.functions.player import update_player
from teikoku.entity.register.player import Player


from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, PrefixHandler


@need_signedup_player
async def set_attr_player(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Define valores de atributos do player por meio de argumentos na
    mensagem.
    """

    args = context.args
    section_name = FAIL_UPDATE_PLAYER_SECTION_NAME
    if not args:  # SEM ARGUMENTOS
        reply_text = FAIL_UPDATE_NOT_ARGS_FORMAT.format(
            attrs=(
                f"{', '.join((f'`{a}`' for a in Player.UPDATABLE_ATTR_LIST))}"
            )
        )
    else:  # UPDATE COM ARGUMENTOS
        formated_args = format_args(args)
        player = update_player(args=formated_args, update=update)

        if player:  # UPDATE COM SUCESSO
            section_name = UPDATE_PLAYER_SECTION_NAME
            player_telegram_text = player.telegram_text
            subsection = format_subsection(text=PLAYER_SUBSECTION_NAME)
            reply_text = f"{subsection}" f"{player_telegram_text}"
        else:  # UPDATE SEM SUCESSO
            reply_text = f"{NO_CHANGE_IN_PLAYER_MSG}"

    reply_text = create_text_in_box(text=reply_text, section_name=section_name)
    await reply_message(
        function_caller="SET_ATTR_PLAYER()",
        text=reply_text,
        context=context,
        update=update,
        markdown=True,
        auto_delete_message=MIN_AUTODELETE_TIME,
    )


SET_PLAYER_HANDLERS = [
    # SET ATTR PLAYER
    PrefixHandler(
        PREFIX_COMMANDS,
        SET_ATTR_PLAYER_COMMANDS,
        set_attr_player,
        BASIC_COMMAND_FILTER,
    ),
    CommandHandler(
        SET_ATTR_PLAYER_COMMANDS, set_attr_player, BASIC_COMMAND_FILTER
    ),
]
