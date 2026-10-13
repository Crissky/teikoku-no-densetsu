from bot.constants.command import SET_ATTR_PLAYER_COMMANDS
from bot.constants.filter import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.constants.message import (
    FAIL_UPDATE_NOT_ARGS_FORMAT,
    NO_CHANGE_IN_PLAYER_MSG,
)
from bot.constants.section import (
    FAIL_UPDATE_PLAYER_SECTION_NAME,
    UPDATE_PLAYER_SECTION_NAME,
)
from bot.decorators.player import need_signedup_player
from bot.functions.arg import format_args
from bot.functions.message import MIN_AUTODELETE_TIME, reply_message
from bot.functions.player import player_telegram_text
from repository.mongo.functions.player import update_player
from teikoku.entity.register.player import Player


from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, PrefixHandler


@need_signedup_player
async def set_attr_player(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Define valores de atributos do player por meio de argumentos na
    mensagem.
    """

    user_id = update.effective_user.id
    args = context.args
    section_name = FAIL_UPDATE_PLAYER_SECTION_NAME
    player = None
    player_not_found_msg = None
    if not args:  # SEM ARGUMENTOS
        updatable_attr_types = Player.updatable_attr_types()
        player_not_found_msg = FAIL_UPDATE_NOT_ARGS_FORMAT.format(
            attrs=", ".join(
                f"`{a}` ({t.__name__})"
                for a, t in updatable_attr_types.items()
            )
        )
    else:  # UPDATE COM ARGUMENTOS
        formated_args = format_args(args)
        player = update_player(args=formated_args, update=update)

        if player:  # UPDATE COM SUCESSO
            section_name = UPDATE_PLAYER_SECTION_NAME
        else:  # UPDATE SEM SUCESSO
            player_not_found_msg = f"{NO_CHANGE_IN_PLAYER_MSG}"

    reply_text = player_telegram_text(
        player=player,
        user_id=user_id,
        section_name=section_name,
        player_not_found_msg=player_not_found_msg,
    )
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
