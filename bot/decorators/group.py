import logging

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants.section import (
    NOT_IS_GROUP_SECTION_NAME,
)
from bot.functions.message import MIN_AUTODELETE_TIME, reply_message
from general.functions.text import create_text_in_box
from repository.mongo.functions.group import chat_is_group

logger = logging.getLogger(__name__)


def only_group(callback):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.info("@NEED_GROUP")
        is_group = chat_is_group(update=update)

        if not is_group:
            logger.info("\tNEGADO - USUÁRIO NÃO POSSUI CONTA.")
            section_name = NOT_IS_GROUP_SECTION_NAME
            text = "Esse comando só pode ser usado em um grupo."
            text = create_text_in_box(text=text, section_name=section_name)
            await reply_message(
                function_caller="ONLY_GROUP()",
                text=text,
                context=context,
                update=update,
                markdown=True,
                allow_sending_without_reply=True,
                need_response=False,
                skip_retry=False,
                auto_delete_message=MIN_AUTODELETE_TIME,
            )

            return ConversationHandler.END
        else:
            logger.info("\tAUTORIZADO - USUÁRIO POSSUI CONTA.")
            return await callback(update, context)

    return wrapper
