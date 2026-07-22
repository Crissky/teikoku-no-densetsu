from bot.constants.alert import ALERT_TEXT_ACCESS_DENIED
from bot.constants.command import SIGNUP_WORLD_COMMANDS, WORLD_COMMANDS
from bot.constants.filter import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.constants.message import (
    WORLD_ARGS_COUNT_ERROR,
    WORLD_ARGS_TYPE_ERROR,
    WORLD_NOT_FOUND_ERROR,
    WORLD_UNKNOWN_ERROR,
)
from bot.constants.section import (
    FAIL_SHOW_WORLD_SECTION_NAME,
    WORLD_SECTION_NAME,
)
from bot.conversations.register import signup_world
from bot.decorators.player import alert_if_not_chat_owner, need_signedup_player
from bot.functions.image import image_to_bytes_io
from bot.functions.message import reply_message, send_message_image
from general.functions.text import create_text_in_box
from repository.mongo.functions.world import get_world_by_chat_id
from teikoku.util.coor import Coordinate


from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, PrefixHandler


# @need_signedup_world
@need_signedup_player
@alert_if_not_chat_owner(alert_text=ALERT_TEXT_ACCESS_DENIED)
async def show_world(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update._effective_chat.id
    args = context.args
    world = get_world_by_chat_id(chat_id=chat_id)

    if not world:
        command = SIGNUP_WORLD_COMMANDS[0]
        reply_text = WORLD_NOT_FOUND_ERROR.format(
            chat_id=chat_id, command=command
        )
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
    elif len(args) == 0:
        image = world.render_map()
        bimagem = image_to_bytes_io(image=image)
        section_name = WORLD_SECTION_NAME
        caption_text = world.telegram_text
        caption_text = create_text_in_box(
            text=caption_text, section_name=section_name
        )
        await send_message_image(
            function_caller="SHOW_WORLD()",
            photo=bimagem,
            context=context,
            caption=caption_text,
            markdown=True,
        )
    elif len(args) == 2:
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
            caption_text = world.telegram_text
            caption_text = create_text_in_box(
                text=caption_text, section_name=section_name
            )
            await send_message_image(
                function_caller="SHOW_WORLD()",
                photo=bimagem,
                context=context,
                caption=caption_text,
                markdown=True,
            )
    elif len(args) not in (0, 2):
        command = WORLD_COMMANDS[0]
        reply_text = WORLD_ARGS_COUNT_ERROR.format(command=command)
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
        WORLD_UNKNOWN_ERROR.format(chat_id=chat_id, args=args, world=world)
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


INFO_WORLD_HANDLERS = [
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
