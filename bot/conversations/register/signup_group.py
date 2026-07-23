from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    PrefixHandler,
)

from bot.constants.command import (
    SIGNUP_GROUP_COMMANDS,
)
from bot.constants.filter import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.constants.message import (
    GROUP_ALREADY_REGISTERED_ERROR,
    GROUP_SUCCESSFULLY_REGISTERED_FORMAT,
)
from bot.constants.section import (
    FAIL_SIGNUP_GROUP_SECTION_NAME,
    GROUP_SUBSECTION_NAME,
    SIGNUP_GROUP_SECTION_NAME,
)
from bot.decorators.group import only_group
from bot.decorators.player import need_admin_player
from bot.functions.message import (
    reply_message,
)
from general.functions.text import create_text_in_box, format_subsection
from repository.mongo.functions.group import (
    exists_group,
    save_group,
)
from teikoku.entity.register.group import Group


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
        reply_text = GROUP_ALREADY_REGISTERED_ERROR.format(id=chat_id)
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


SIGNUP_GROUP_HANDLERS = [
    # SIGNUP_GROUP
    PrefixHandler(
        PREFIX_COMMANDS,
        SIGNUP_GROUP_COMMANDS,
        signup_group,
        BASIC_COMMAND_FILTER,
    ),
    CommandHandler(SIGNUP_GROUP_COMMANDS, signup_group, BASIC_COMMAND_FILTER),
]
