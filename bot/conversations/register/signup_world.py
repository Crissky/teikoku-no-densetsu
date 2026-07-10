from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, PrefixHandler

from bot.constants.command import SIGNUP_WORLD_COMMANDS
from bot.constants.filter import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.constants.message import (
    WORLD_SUCCESSFULLY_REGISTERED_FORMAT,
)
from bot.constants.section import (
    FAIL_SIGNUP_WORLD_SECTION_NAME,
    WORLD_SECTION_NAME,
    WORLD_SUBSECTION_NAME,
)
from bot.functions.message import (
    CHAT_TYPE_PRIVATE,
    reply_message,
)
from general.functions.text import create_text_in_box, format_subsection
from repository.mongo.functions.world import get_world_by_chat_id, save_world
from teikoku.entity.world.world import World


async def signup_world(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cadastra Mundo"""

    chat = update._effective_chat
    chat_id = chat.id
    chat_name = chat.full_name or chat.title
    reply_text = ""

    world = get_world_by_chat_id(chat_id=chat_id)
    if world:
        section_name = FAIL_SIGNUP_WORLD_SECTION_NAME
        reply_text = f'O mundo "{world.name}" já existe.'
    if chat.type in CHAT_TYPE_PRIVATE:
        section_name = FAIL_SIGNUP_WORLD_SECTION_NAME
        command = SIGNUP_WORLD_COMMANDS[0]
        reply_text = (
            "Não é possível criar um mundo em um chat privado. "
            f"Use o comando /{command} no grupo que deseja cadastrar."
        )
    else:
        world = World(name=chat_name, chat_id=chat_id)
        new_world = save_world(world=world)
        section_name = WORLD_SECTION_NAME
        world_telegram_text = new_world.telegram_text
        subsection = format_subsection(text=WORLD_SUBSECTION_NAME)
        reply_text = WORLD_SUCCESSFULLY_REGISTERED_FORMAT.format(
            name=new_world.name,
            subsection=subsection,
            telegram_text=world_telegram_text,
        )

    reply_text = create_text_in_box(text=reply_text, section_name=section_name)
    await reply_message(
        function_caller="SIGNUP_WORLD()",
        text=reply_text,
        context=context,
        update=update,
        markdown=True,
    )


SIGNUP_WORLD_HANDLERS = [
    # SIGNUP_GROUP
    PrefixHandler(
        PREFIX_COMMANDS,
        SIGNUP_WORLD_COMMANDS,
        signup_world,
        BASIC_COMMAND_FILTER,
    ),
    CommandHandler(SIGNUP_WORLD_COMMANDS, signup_world, BASIC_COMMAND_FILTER),
]
