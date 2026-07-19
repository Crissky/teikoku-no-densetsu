from bot.constants.command import GROUP_COMMANDS
from bot.constants.filter import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.constants.query import (
    CALLBACK_COMMAND_REFRESH_GROUP,
    CALLBACK_COMMAND_UPDATE_GROUP,
)
from bot.constants.section import (
    GROUP_SECTION_NAME,
    REFRESH_GROUP_SECTION_NAME,
    UPDATE_GROUP_SECTION_NAME,
)
from bot.decorators.group import only_group
from bot.decorators.player import need_admin_player
from bot.functions.group import group_telegram_text
from bot.functions.handler import check_pattern
from bot.functions.message import (
    MIN_AUTODELETE_TIME,
    callback_data_to_dict,
    edit_message_text,
    get_refresh_update_close_keyboard,
    reply_message,
)
from repository.mongo.functions.group import get_group, save_group


from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    PrefixHandler,
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


INFO_GROUP_HANDLERS = [
    # SHOW_GROUP
    PrefixHandler(
        PREFIX_COMMANDS, GROUP_COMMANDS, show_group, BASIC_COMMAND_FILTER
    ),
    CommandHandler(GROUP_COMMANDS, show_group, BASIC_COMMAND_FILTER),
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
]
