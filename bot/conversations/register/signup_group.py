from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, PrefixHandler

from bot.constants.command import SIGNUP_GROUP_COMMNADS
from bot.constants.filter import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.constants.section import (
    GROUP_SUBSECTION_NAME,
    SIGNUP_GROUP_SECTION_NAME,
)
from bot.decorators.group import only_group
from bot.decorators.player import need_admin_player
from bot.functions.message import reply_message
from general.functions.text import create_text_in_box, format_subsection
from repository.mongo.functions.group import exists_group, save_group
from teikoku.register.group import Group


@only_group
@need_admin_player
async def signup_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update._effective_chat
    chat_id = chat.id
    chat_name = chat.full_name or chat.title
    group = Group(chat_id=chat_id, name=chat_name)

    if exists_group(chat_id=chat_id):
        reply_text = f"Grupo com CHAT ID: '{chat_id}', já está cadastrado."
    else:
        new_group = save_group(group=group)
        group_telegram_text = new_group.telegram_text
        subsection = format_subsection(text=GROUP_SUBSECTION_NAME)
        reply_text = (
            f"Grupo cadastrado com sucesso!\n\n"
            f"{subsection}"
            f"{group_telegram_text}"
        )

    reply_text = create_text_in_box(
        text=reply_text, section_name=SIGNUP_GROUP_SECTION_NAME
    )
    await reply_message(
        function_caller="SIGNUP()",
        text=reply_text,
        context=context,
        update=update,
        markdown=True,
    )


async def show_group(update: Update, context: ContextTypes.DEFAULT_TYPE): ...
async def update_group(update: Update, context: ContextTypes.DEFAULT_TYPE): ...


SIGNUP_GROUP_HANDLERS = [
    PrefixHandler(
        PREFIX_COMMANDS,
        SIGNUP_GROUP_COMMNADS,
        signup_group,
        BASIC_COMMAND_FILTER,
    ),
    CommandHandler(SIGNUP_GROUP_COMMNADS, signup_group, BASIC_COMMAND_FILTER),
]
