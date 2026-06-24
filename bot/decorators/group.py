import logging

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.functions.message import MIN_AUTODELETE_TIME, reply_message
from repository.mongo.functions.group import chat_is_group

logger = logging.getLogger(__name__)


def only_group(callback):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.info("@NEED_GROUP")
        is_group = chat_is_group(update=update)

        if not is_group:
            logger.info("\tNEGADO - USUÁRIO NÃO POSSUI CONTA.")
            text = "Esse comando só pode ser usado em um grupo."
            await reply_message(
                function_caller="ONLY_GROUP()",
                text=text,
                context=context,
                update=update,
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
