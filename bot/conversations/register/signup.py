from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    PrefixHandler,
    CommandHandler,
)

from bot.constants.alert import ALERT_TEXT_ACCESS_DENIED
from bot.constants.command import (
    PLAYER_COMMNADS,
    SIGNUP_COMMNADS,
    SET_ATTR_PLAYER_COMMNADS,
)
from bot.constants.filter import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.constants.message import (
    FAIL_UPDATE_NOT_ARGS_FORMAT,
    NO_CHANGE_IN_PLAYER,
    PLAYER_ALREADY_REGISTERED_FORMAT,
    PLAYER_SUCCESSFULLY_REGISTERED_FORMAT,
)
from bot.constants.query import (
    CALLBACK_COMMAND_REFRESH_PLAYER,
    CALLBACK_COMMAND_UPDATE_PLAYER,
)
from bot.constants.section import (
    FAIL_SIGNUP_SECTION_NAME,
    FAIL_UPDATE_PLAYER_SECTION_NAME,
    PLAYER_SECTION_NAME,
    PLAYER_SUBSECTION_NAME,
    REFRESH_PLAYER_SECTION_NAME,
    SIGNUP_SECTION_NAME,
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
from bot.functions.arg import format_args
from bot.functions.user import get_username
from bot.functions.player import player_telegram_text
from general.functions.text import create_text_in_box, format_subsection
from repository.mongo.functions.player import (
    exists_player,
    get_player,
    save_player,
    update_player,
)
from teikoku.register.player import Player


async def signup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cadastro do player."""

    user_id = update.effective_user.id
    full_name = update.effective_user.full_name
    username = get_username(update=update)
    player = Player(user_id=user_id, name=full_name, username=username)

    if exists_player(player.user_id):  # JÁ CADASTRADO
        section_name = FAIL_SIGNUP_SECTION_NAME
        reply_text = PLAYER_ALREADY_REGISTERED_FORMAT.format(id=player.user_id)
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
            reply_text = f"{NO_CHANGE_IN_PLAYER}"

    reply_text = create_text_in_box(text=reply_text, section_name=section_name)
    await reply_message(
        function_caller="SET_ATTR_PLAYER()",
        text=reply_text,
        context=context,
        update=update,
        markdown=True,
        auto_delete_message=MIN_AUTODELETE_TIME,
    )


SIGNUP_HANDLERS = [
    # SIGNUP
    PrefixHandler(
        PREFIX_COMMANDS, SIGNUP_COMMNADS, signup, BASIC_COMMAND_FILTER
    ),
    CommandHandler(SIGNUP_COMMNADS, signup, BASIC_COMMAND_FILTER),
    # SHOW_PLAYER
    PrefixHandler(
        PREFIX_COMMANDS, PLAYER_COMMNADS, show_player, BASIC_COMMAND_FILTER
    ),
    CommandHandler(PLAYER_COMMNADS, show_player, BASIC_COMMAND_FILTER),
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
    # SET ATTR PLAYER
    PrefixHandler(
        PREFIX_COMMANDS,
        SET_ATTR_PLAYER_COMMNADS,
        set_attr_player,
        BASIC_COMMAND_FILTER,
    ),
    CommandHandler(
        SET_ATTR_PLAYER_COMMNADS, set_attr_player, BASIC_COMMAND_FILTER
    ),
]
