from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    PrefixHandler,
)

from bot.constants.command import (
    GROUP_COMMNADS,
    SIGNUP_GROUP_COMMNADS,
    SET_ATTR_GROUP_COMMNADS,
)
from bot.constants.filter import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.constants.message import (
    ALTERABLE_ATTRIBUTES_HEADER,
    FAIL_UPDATE_NOT_ARGS,
    GROUP_ALREADY_REGISTERED_FORMAT,
    GROUP_SUCCESSFULLY_REGISTERED_FORMAT,
    NO_CHANGE_IN_GROUP,
)
from bot.constants.query import (
    CALLBACK_COMMAND_REFRESH_GROUP,
    CALLBACK_COMMAND_UPDATE_GROUP,
)
from bot.constants.section import (
    FAIL_SIGNUP_GROUP_SECTION_NAME,
    FAIL_UPDATE_GROUP_SECTION_NAME,
    GROUP_SECTION_NAME,
    GROUP_SUBSECTION_NAME,
    REFRESH_GROUP_SECTION_NAME,
    SIGNUP_GROUP_SECTION_NAME,
    UPDATE_GROUP_SECTION_NAME,
)
from bot.decorators.group import only_group
from bot.decorators.player import need_admin_player
from bot.functions.arg import format_args
from bot.functions.group import group_telegram_text
from bot.functions.handler import check_pattern
from bot.functions.message import (
    MIN_AUTODELETE_TIME,
    callback_data_to_dict,
    edit_message_text,
    get_refresh_update_close_keyboard,
    reply_message,
)
from general.functions.text import create_text_in_box, format_subsection
from repository.mongo.functions.group import (
    exists_group,
    get_group,
    save_group,
    update_group,
)
from teikoku.register.group import Group


@only_group
@need_admin_player
async def signup_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cadastro do Grupo."""

    chat = update._effective_chat
    chat_id = chat.id
    chat_name = chat.full_name or chat.title
    group = Group(chat_id=chat_id, name=chat_name)

    if exists_group(chat_id=chat_id):
        section_name = FAIL_SIGNUP_GROUP_SECTION_NAME
        reply_text = GROUP_ALREADY_REGISTERED_FORMAT.format(id=chat_id)
    else:
        section_name = SIGNUP_GROUP_SECTION_NAME
        new_group = save_group(group=group)
        group_telegram_text = new_group.telegram_text
        subsection = format_subsection(text=GROUP_SUBSECTION_NAME)
        reply_text = GROUP_SUCCESSFULLY_REGISTERED_FORMAT.format(
            name=new_group.name,
            subsection=subsection,
            telegram_text=group_telegram_text,
        )

    reply_text = create_text_in_box(text=reply_text, section_name=section_name)
    await reply_message(
        function_caller="SIGNUP_GROUP()",
        text=reply_text,
        context=context,
        update=update,
        markdown=True,
    )


@only_group
@need_admin_player
async def show_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Exibe os dados do group e gerencia a recarga da exibição e atualiza as
    informações básicas do group.
    """

    query = update.callback_query
    group = get_group(update=update)
    func_message = reply_message
    section_name = GROUP_SECTION_NAME
    func_message_kwargs = dict(
        function_caller="SHOW_GROUP()",
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
        if command == CALLBACK_COMMAND_REFRESH_GROUP:
            section_name = REFRESH_GROUP_SECTION_NAME
        elif command == CALLBACK_COMMAND_UPDATE_GROUP:
            section_name = UPDATE_GROUP_SECTION_NAME
            chat = update._effective_chat
            group.name = chat.full_name or chat.title
            group = save_group(group)

    reply_text = group_telegram_text(group=group, section_name=section_name)
    reply_markup = get_refresh_update_close_keyboard(
        user_id=update.effective_user.id,
        refresh_command=CALLBACK_COMMAND_REFRESH_GROUP,
        update_command=CALLBACK_COMMAND_UPDATE_GROUP,
    )
    func_message_kwargs.update(
        dict(
            text=reply_text,
            reply_markup=reply_markup,
        )
    )

    await func_message(**func_message_kwargs)


@only_group
@need_admin_player
async def set_attr_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Define valores de atributos do group por meio de argumentos na
    mensagem.
    """

    args = context.args
    section_name = FAIL_UPDATE_GROUP_SECTION_NAME
    if not args:  # SEM ARGUMENTOS
        reply_text = (
            f"{FAIL_UPDATE_NOT_ARGS}"
            f"{ALTERABLE_ATTRIBUTES_HEADER}"
            f"{', '.join((f'`{a}`' for a in Group.UPDATABLE_ATTR_LIST))}"
        )
    else:  # UPDATE COM ARGUMENTOS
        formated_args = format_args(args)
        group = update_group(args=formated_args, update=update)

        if group:  # UPDATE COM SUCESSO
            section_name = UPDATE_GROUP_SECTION_NAME
            group_telegram_text = group.telegram_text
            subsection = format_subsection(text=GROUP_SUBSECTION_NAME)
            reply_text = f"{subsection}" f"{group_telegram_text}"
        else:  # UPDATE SEM SUCESSO
            reply_text = f"{NO_CHANGE_IN_GROUP}"

    reply_text = create_text_in_box(text=reply_text, section_name=section_name)
    await reply_message(
        function_caller="SET_ATTR_GROUP()",
        text=reply_text,
        context=context,
        update=update,
        markdown=True,
        auto_delete_message=MIN_AUTODELETE_TIME,
    )


SIGNUP_GROUP_HANDLERS = [
    # SIGNUP_GROUP
    PrefixHandler(
        PREFIX_COMMANDS,
        SIGNUP_GROUP_COMMNADS,
        signup_group,
        BASIC_COMMAND_FILTER,
    ),
    CommandHandler(SIGNUP_GROUP_COMMNADS, signup_group, BASIC_COMMAND_FILTER),
    # SHOW_GROUP
    PrefixHandler(
        PREFIX_COMMANDS, GROUP_COMMNADS, show_group, BASIC_COMMAND_FILTER
    ),
    CommandHandler(GROUP_COMMNADS, show_group, BASIC_COMMAND_FILTER),
    CallbackQueryHandler(
        show_group,
        pattern=check_pattern(
            f'"{CALLBACK_COMMAND_REFRESH_GROUP}"', _match=False
        ),
    ),
    CallbackQueryHandler(
        show_group,
        pattern=check_pattern(
            f'"{CALLBACK_COMMAND_UPDATE_GROUP}"', _match=False
        ),
    ),
    # SET ATTR GROUP
    PrefixHandler(
        PREFIX_COMMANDS,
        SET_ATTR_GROUP_COMMNADS,
        set_attr_group,
        BASIC_COMMAND_FILTER,
    ),
    CommandHandler(
        SET_ATTR_GROUP_COMMNADS, set_attr_group, BASIC_COMMAND_FILTER
    ),
]
