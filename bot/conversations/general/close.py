import logging

from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
)

from bot.constants.close import ACCESS_DENIED
from bot.constants.query import CALLBACK_COMMAND_CLOSE
from bot.decorators.player import (
    alert_if_not_chat_owner,
    skip_if_no_singup_player,
)
from bot.decorators.print import print_basic_infos


from bot.functions.handler import check_pattern
from bot.functions.messages import (
    answer,
    delete_message_from_query,
    remove_job_delete_message_from_context,
)

logger = logging.getLogger(__name__)


@alert_if_not_chat_owner(alert_text=ACCESS_DENIED)
@print_basic_infos
@skip_if_no_singup_player
async def close(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fecha uma mensagem."""

    logger.info("CLOSE() - FECHANDO MENSAGEM")
    query = update.callback_query

    if query:
        chat_id = query.message.chat_id
        message_id = query.message.message_id
        await answer(query=query, text="Fechando conversa...")
        await delete_message_from_query(
            function_caller="CLOSE()",
            context=context,
            query=query,
        )
        remove_job_delete_message_from_context(
            context=context, chat_id=chat_id, message_id=message_id
        )


CLOSE_MSG_HANDLER = CallbackQueryHandler(
    close, pattern=check_pattern(f'"{CALLBACK_COMMAND_CLOSE}"', _match=False)
)
