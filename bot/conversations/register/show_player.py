from bot.constants.alert import ALERT_TEXT_ACCESS_DENIED
from bot.constants.command import PLAYER_COMMANDS
from bot.constants.filter import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.constants.query import (
    CALLBACK_COMMAND_REFRESH_PLAYER,
    CALLBACK_COMMAND_UPDATE_PLAYER,
)
from bot.constants.section import (
    PLAYER_SECTION_NAME,
    REFRESH_PLAYER_SECTION_NAME,
    UPDATE_PLAYER_SECTION_NAME,
)
from bot.decorators.player import alert_if_not_chat_owner, need_signedup_player
from bot.functions.handler import check_pattern
from bot.functions.message import (
    MIN_AUTODELETE_TIME,
    callback_data_to_dict,
    edit_message_text,
    get_refresh_update_close_keyboard,
    reply_message,
)
from bot.functions.player import player_telegram_text
from bot.functions.user import get_username
from repository.mongo.functions.player import get_player, save_player


from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    PrefixHandler,
)


@need_signedup_player
@alert_if_not_chat_owner(alert_text=ALERT_TEXT_ACCESS_DENIED)
async def show_player(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Exibe os dados do player e gerencia a recarga da exibição e atualiza as
    informações básicas do player.
    """

    query = update.callback_query
    player = get_player(update=update)
    func_message = reply_message
    section_name = PLAYER_SECTION_NAME
    func_message_kwargs = dict(
        function_caller="SHOW_PLAYER()",
        context=context,
        update=update,
        markdown=True,
        auto_delete_message=MIN_AUTODELETE_TIME,
    )

    if query:  # UPDATE OR REFRESH BUTTON
        func_message_kwargs.pop("auto_delete_message")
        func_message = edit_message_text
        data = callback_data_to_dict(query.data)
        command = data.get("command")
        if command == CALLBACK_COMMAND_REFRESH_PLAYER:
            section_name = REFRESH_PLAYER_SECTION_NAME
        elif command == CALLBACK_COMMAND_UPDATE_PLAYER:
            section_name = UPDATE_PLAYER_SECTION_NAME
            player.name = update.effective_user.full_name
            player.username = get_username(update=update)
            player = save_player(player)

    reply_text = player_telegram_text(player=player, section_name=section_name)
    reply_markup = get_refresh_update_close_keyboard(
        user_id=player.user_id,
        refresh_command=CALLBACK_COMMAND_REFRESH_PLAYER,
        update_command=CALLBACK_COMMAND_UPDATE_PLAYER,
    )
    func_message_kwargs.update(
        dict(
            text=reply_text,
            reply_markup=reply_markup,
        )
    )

    await func_message(**func_message_kwargs)


SIGNUP_PLAYER_HANDLERS = [
    # SHOW_PLAYER
    PrefixHandler(
        PREFIX_COMMANDS, PLAYER_COMMANDS, show_player, BASIC_COMMAND_FILTER
    ),
    CommandHandler(PLAYER_COMMANDS, show_player, BASIC_COMMAND_FILTER),
    CallbackQueryHandler(
        show_player,
        pattern=check_pattern(
            f'"{CALLBACK_COMMAND_REFRESH_PLAYER}"', _match=False
        ),
    ),
    CallbackQueryHandler(
        show_player,
        pattern=check_pattern(
            f'"{CALLBACK_COMMAND_UPDATE_PLAYER}"', _match=False
        ),
    ),
]
