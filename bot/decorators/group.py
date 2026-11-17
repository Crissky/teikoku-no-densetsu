import logging

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants.command import SIGNUP_GROUP_COMMANDS
from bot.constants.section import (
    NOT_FOUND_GROUP_SECTION_NAME,
    NOT_IS_GROUP_SECTION_NAME,
)
from bot.functions.message import MIN_AUTODELETE_TIME, reply_message
from general.functions.text import create_text_in_box
from repository.mongo.functions.group import chat_is_group
from repository.mongo.models.group import GroupModel

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


def need_signedup_group(callback):
    """Decorador para verificação de grupo cadastrado.

    Não excuta a ação se o grupo não estiver cadastrado e
    responde com mensagem informando a necessidade do cadastro.
    """

    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.info("@NEED_SIGNEDUP_GROUP")
        group_model = GroupModel()
        chat_id = update.effective_chat.id

        if group_model.exists(chat_id):
            logger.info("\tAUTORIZADO - GRUPO POSSUI CONTA.")
            return await callback(update, context)
        else:
            logger.info("\tNEGADO - GRUPO NÃO POSSUI CONTA.")
            command = SIGNUP_GROUP_COMMANDS[0]
            text = (
                "O Grupo precisa ter uma conta "
                "para utilizar esse comando.\n"
                f"Crie a conta com o comando /{command}."
            )
            section_name = NOT_FOUND_GROUP_SECTION_NAME
            text = create_text_in_box(text=text, section_name=section_name)
            await reply_message(
                function_caller="@NEED_SIGNEDUP_GROUP()",
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

    return wrapper
