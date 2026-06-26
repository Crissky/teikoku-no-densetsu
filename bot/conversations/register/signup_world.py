from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, PrefixHandler

from bot.constants.alert import ALERT_TEXT_ACCESS_DENIED
from bot.constants.command import SIGNUP_WORLD_COMMANDS, WORLD_COMMANDS
from bot.constants.filter import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.constants.message import (
    WORLD_ARGS_TYPE_ERROR,
    WORLD_SUCCESSFULLY_REGISTERED_FORMAT,
)
from bot.constants.section import (
    FAIL_SHOW_WORLD_SECTION_NAME,
    FAIL_SIGNUP_WORLD_SECTION_NAME,
    WORLD_SECTION_NAME,
    WORLD_SUBSECTION_NAME,
)
from bot.decorators.player import alert_if_not_chat_owner, need_signedup_player
from bot.decorators.world import need_signedup_world
from bot.functions.image import image_to_bytes_io
from bot.functions.message import (
    CHAT_TYPE_PRIVATE,
    reply_message,
    send_message_image,
)
from general.functions.text import create_text_in_box, format_subsection
from repository.mongo.functions.world import get_world_by_chat_id, save_world
from teikoku.entity.world.coor import Coordinate
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


@need_signedup_world
@need_signedup_player
@alert_if_not_chat_owner(alert_text=ALERT_TEXT_ACCESS_DENIED)
async def show_world(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update._effective_chat.id
    args = context.args if context.args else [0, 0]
    world = get_world_by_chat_id(chat_id=chat_id)

    if len(args) == 2:
        try:
            x = int(args[0])
            y = int(args[1])
        except ValueError:
            command = WORLD_COMMANDS[0]
            reply_text = WORLD_ARGS_TYPE_ERROR.format(command=command)
            reply_text = create_text_in_box(
                text=reply_text, section_name=FAIL_SHOW_WORLD_SECTION_NAME
            )
            await reply_message(
                function_caller="SHOW_WORLD()",
                text=reply_text,
                context=context,
                update=update,
                markdown=True,
            )
        else:
            coordinate = Coordinate(x=x, y=y)
            image = world.render_map(central_coor=coordinate)
            bimagem = image_to_bytes_io(image=image)
            section_name = WORLD_SECTION_NAME
            caption_text = str(world)
            caption_text = create_text_in_box(
                text=caption_text, section_name=section_name
            )
            await send_message_image(
                function_caller="SHOW_WORLD()",
                photo=bimagem,
                context=context,
                caption=caption_text,
            )
    # TODO Adicionar error por quantidade de argumentos inválidos.
    else:
        ...


SIGNUP_WORLD_HANDLERS = [
    # SIGNUP_GROUP
    PrefixHandler(
        PREFIX_COMMANDS,
        SIGNUP_WORLD_COMMANDS,
        signup_world,
        BASIC_COMMAND_FILTER,
    ),
    CommandHandler(SIGNUP_WORLD_COMMANDS, signup_world, BASIC_COMMAND_FILTER),
    # SHOW_GROUP
    PrefixHandler(
        PREFIX_COMMANDS, WORLD_COMMANDS, show_world, BASIC_COMMAND_FILTER
    ),
    CommandHandler(WORLD_COMMANDS, show_world, BASIC_COMMAND_FILTER),
    # CallbackQueryHandler(
    #     show_group,
    #     pattern=check_pattern(
    #         f'"{CALLBACK_COMMAND_REFRESH_GROUP}"', _match=False
    #     ),
    # ),
    # CallbackQueryHandler(
    #     show_group,
    #     pattern=check_pattern(
    #         f'"{CALLBACK_COMMAND_UPDATE_GROUP}"', _match=False
    #     ),
    # ),
]
