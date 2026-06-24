import logging

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants.command import SIGNUP_WORLD_COMMANDS
from bot.functions.message import MIN_AUTODELETE_TIME, reply_message
from repository.mongo.models.world import WorldModel

logger = logging.getLogger(__name__)


def need_signedup_world(callback):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.info("@NEED_SIGNEDUP_WORLD")
        world_model = WorldModel()
        chat_id = update.effective_chat.id

        if world_model.exists(chat_id):
            logger.info("\t AUTORIZADO - CHAT POSSUI UM MUNDO.")
            return await callback(update, context)
        else:
            logger.info("\tNEGADO - CHAT NÃO POSSUI MUNDO.")
            command = SIGNUP_WORLD_COMMANDS[0]
            text = (
                "Este grupo ainda não possui um mundo."
                f"Crie UM MUNDO com o comando /{command}."
            )
            await reply_message(
                function_caller="@NEED_SIGNEDUP_WORLD()",
                text=text,
                context=context,
                update=update,
                allow_sending_without_reply=True,
                need_response=False,
                skip_retry=False,
                auto_delete_message=MIN_AUTODELETE_TIME,
            )

            return ConversationHandler.END

    return wrapper
