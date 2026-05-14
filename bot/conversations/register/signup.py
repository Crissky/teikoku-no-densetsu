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
    UPDATE_PLAYER_COMMNADS,
)
from bot.constants.filter import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.constants.message import FAIL_UPDATE_NOT_ARGS
from bot.constants.query import (
    CALLBACK_COMMAND_REFRESH_PLAYER,
    CALLBACK_COMMAND_UPDATE_PLAYER,
)
from bot.constants.section import (
    FAIL_UPDATE_PLAYER_SECTION_NAME,
    PLAYER_SECTION_NAME,
    PLAYER_SUBSECTION_NAME,
    REFRESH_PLAYER_SECTION_NAME,
    SIGNUP_SECTION_NAME,
    UPDATE_PLAYER_SECTION_NAME,
)
from bot.decorators.player import alert_if_not_chat_owner, need_singup_player
from bot.functions.handler import check_pattern
from bot.functions.message import (
    MIN_AUTODELETE_TIME,
    callback_data_to_dict,
    edit_message_text,
    get_refresh_update_close_keyboard,
    reply_message,
)
from bot.functions.update import format_args
from bot.functions.user import get_username
from bot.functions.player import player_telegram_text
from general.functions.text import create_text_in_box, format_subsection
from repository.mongo.functions.player import (
    exists_player,
    get_player,
    save_player,
)
from teikoku.register.player import Player


async def signup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cadastro do player."""

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
        auto_delete_message=MIN_AUTODELETE_TIME,
    )


@need_singup_player
@alert_if_not_chat_owner(alert_text=ALERT_TEXT_ACCESS_DENIED)
async def show_player(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Exibe os dados do player e gerencia a recarga da exibição e atualiza as
    informações básicas do player.
    """

    query = update.callback_query
    player = get_player(update=update)
    func_message = reply_message
    section_name = PLAYER_SECTION_NAME

    if query:  # UPDATE OR REFRESH BUTTON
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
    func_message_kwargs = dict(
        function_caller="SHOW_PLAYER()",
        text=reply_text,
        context=context,
        update=update,
        markdown=True,
        reply_markup=reply_markup,
        auto_delete_message=MIN_AUTODELETE_TIME,
    )
    func_message_kwargs

    await func_message(**func_message_kwargs)


@need_singup_player
async def update_player(update: Update, context: ContextTypes.DEFAULT_TYPE):

    args = context.args
    if not args:
        section_name = FAIL_UPDATE_PLAYER_SECTION_NAME
        reply_text = (
            f"{FAIL_UPDATE_NOT_ARGS}"
            "Atributos alteráveis do jogador:\n"
            f"{', '.join((f'`{a}`' for a in Player.UPDATABLE_ATTR_LIST))}"
        )
    else:
        formated_args = format_args(args)
        section_name = UPDATE_PLAYER_SECTION_NAME
        reply_text = "COMANDO NÃO IMPLEMENTADO!!!"

    reply_text = create_text_in_box(
        text=reply_text, section_name=section_name
    )
    await reply_message(
        function_caller="UPDATE_PLAYER()",
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
    # UPDATE PLAYER
    PrefixHandler(
        PREFIX_COMMANDS,
        UPDATE_PLAYER_COMMNADS,
        update_player,
        BASIC_COMMAND_FILTER,
    ),
    CommandHandler(
        UPDATE_PLAYER_COMMNADS, update_player, BASIC_COMMAND_FILTER
    ),
]
