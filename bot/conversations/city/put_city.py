from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.command import PUT_CITY
from bot.constants.message import CITY_NO_ARGS_ERROR
from bot.constants.section import FAIL_PUT_CITY_SECTION_NAME
from bot.decorators.player import need_signedup_player
from bot.decorators.world import need_signedup_world
from bot.functions.message import reply_message
from general.functions.text import create_text_in_box


# @need_signedup_world
@need_signedup_player
async def put_dicty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update._effective_chat
    chat_id = chat.id
    args = context.args
    city_name = " ".join(args)

    if not city_name:
        command = PUT_CITY[0]
        section_name = FAIL_PUT_CITY_SECTION_NAME
        reply_text = CITY_NO_ARGS_ERROR.format(command=command)

    reply_text = create_text_in_box(text=reply_text, section_name=section_name)
    await reply_message(
        function_caller="SIGNUP_WORLD()",
        text=reply_text,
        context=context,
        update=update,
        markdown=True,
    )
