from bot.constants.command import SET_ATTR_GROUP_COMMANDS
from bot.constants.filter import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.constants.message import (
    FAIL_UPDATE_NOT_ARGS_FORMAT,
    NO_CHANGE_IN_GROUP_MSG_FORMAT,
)
from bot.constants.section import (
    FAIL_UPDATE_GROUP_SECTION_NAME,
    GROUP_SUBSECTION_NAME,
    UPDATE_GROUP_SECTION_NAME,
)
from bot.decorators.group import only_group
from bot.decorators.player import need_admin_player
from bot.functions.arg import format_args
from bot.functions.group import group_telegram_text
from bot.functions.message import (
    MIN_AUTODELETE_TIME,
    reply_message,
)
from general.functions.text import create_text_in_box, format_subsection
from repository.mongo.functions.group import (
    update_group,
)


from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, PrefixHandler

from teikoku.entity.register.group import Group


@only_group
@need_admin_player
async def set_attr_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Define valores de atributos do group por meio de argumentos na
    mensagem.
    """

    chat_id = update.effective_chat.id
    args = context.args
    section_name = FAIL_UPDATE_GROUP_SECTION_NAME
    group = None
    group_not_found_msg = None
    if not args:  # SEM ARGUMENTOS
        updatable_attr_types = Group.updatable_attr_types()
        reply_text = FAIL_UPDATE_NOT_ARGS_FORMAT.format(
            attrs=", ".join(
                f"`{a}` ({t.__name__})"
                for a, t in updatable_attr_types.items()
            )
        )
    else:  # UPDATE COM ARGUMENTOS
        formated_args = format_args(args)
        group = update_group(args=formated_args, update=update)
        if group:  # UPDATE COM SUCESSO
            section_name = UPDATE_GROUP_SECTION_NAME
        else:  # UPDATE SEM SUCESSO
            updatable_attr_text = Group.updatable_attr_text()
            group_not_found_msg = NO_CHANGE_IN_GROUP_MSG_FORMAT.format(
                attrs=updatable_attr_text
            )

    reply_text = group_telegram_text(
        group=group,
        chat_id=chat_id,
        section_name=section_name,
        group_not_found_msg=group_not_found_msg,
    )
    await reply_message(
        function_caller="SET_ATTR_GROUP()",
        text=reply_text,
        context=context,
        update=update,
        markdown=True,
        auto_delete_message=MIN_AUTODELETE_TIME,
    )


SET_GROUP_HANDLERS = [
    # SET ATTR GROUP
    PrefixHandler(
        PREFIX_COMMANDS,
        SET_ATTR_GROUP_COMMANDS,
        set_attr_group,
        BASIC_COMMAND_FILTER,
    ),
    CommandHandler(
        SET_ATTR_GROUP_COMMANDS, set_attr_group, BASIC_COMMAND_FILTER
    ),
]
