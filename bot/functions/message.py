import logging

from datetime import timedelta
from random import randint
from time import sleep
from typing import Any, Callable, Optional, Union

from bson import ObjectId
from telegram import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ReplyParameters,
    Update,
)
from telegram.constants import ChatType, ParseMode
from telegram.error import BadRequest, RetryAfter, TimedOut
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants.query import CALLBACK_COMMAND_CLOSE
from bot.constants.job import BASE_JOB_KWARGS
from general.enums.emojis import EmojiEnum

logger = logging.getLogger(__name__)


# DATE & TIME ================================================================
HOURS_DELETE_MESSAGE_FROM_CONTEXT = 1
CHAT_TYPE_GROUPS = (ChatType.GROUP, ChatType.SUPERGROUP)
CHAT_TYPE_PRIVATE = (ChatType.SENDER, ChatType.PRIVATE)
MIN_AUTODELETE_TIME = timedelta(minutes=15)
HALF_AUTODELETE_TIME = timedelta(minutes=30)

# TEXTS ======================================================================
REPLY_MARKUP_DEFAULT = "DEFAULT"
LEFT_CLOSE_BUTTON_TEXT = f"{EmojiEnum.CLOSE.value}Fechar"
RIGHT_CLOSE_BUTTON_TEXT = f"Fechar{EmojiEnum.CLOSE.value}"
LEFT_REFRESH_BUTTON_TEXT = f"{EmojiEnum.REFRESH.value}Recarregar"
RIGHT_REFRESH_BUTTON_TEXT = f"Recarregar{EmojiEnum.REFRESH.value}"
LEFT_UPDATE_BUTTON_TEXT = f"{EmojiEnum.UPDATE.value}Atualizar"
RIGHT_UPDATE_BUTTON_TEXT = f"Atualizar{EmojiEnum.UPDATE.value}"
DETAIL_BUTTON_TEXT = f"{EmojiEnum.DETAIL.value}Detalhar"


CALLBACK_KEY_LIST = ["command", "user_id"]


# CALL TEXT TELEGRAM FUNCTIONs ===============================================
async def call_telegram_message_function(
    function_caller: str,
    function: Callable,
    context: ContextTypes.DEFAULT_TYPE,
    need_response: bool = False,
    skip_retry: bool = False,
    auto_delete_message: Union[bool, int, timedelta] = True,
    **kwargs,
) -> Union[Any, Message]:
    """Função que chama qualquer função de mensagem do telegram.
    Caso ocorra um erro do tipo RetryAfter ou TimedOut, a função agurdará
    alguns segundos tentará novamente com um número máximo de 3 tentativas.
    Caso a função retorne um objeto do tipo Message, a mensagem será excluída
    em "HOURS_DELETE_MESSAGE_FROM_CONTEXT" horas.

    Se need_response for True, a função aguardará para realizar uma nova
    tentativa, caso contrário, a função será agendada em um job para ser
    executada posteriormente.

    Se skip_retry for True, a função não tentará novamente e nem agendará uma
    nova tentativa.

    Se auto_delete_message for igual a False, a exclusão automática da
    mensagem será ignorada. Caso seja igual a True, a mensagem será excluída
    em "HOURS_DELETE_MESSAGE_FROM_CONTEXT" horas.
    Mas se for um valor inteiro positivo, a mensagem será excluída em uma
    quantidade de horas igual ao valor passado.
    E se for um timedelta, a mensagem será excluída de acordo com o tempo
    passado no timedelta.
    """

    logger.info(f"{function_caller}->CALL_TELEGRAM_MESSAGE_FUNCTION()")
    job_call_telegram_kwargs = dict(
        function_caller=function_caller,
        function=function,
        context=context,
        **kwargs,
    )
    response = None
    is_error = True
    catched_error = None
    for i in range(3):
        try:
            response = await function(**kwargs)
            is_error = False
            break
        except (RetryAfter, TimedOut) as error:
            catched_error = error
            error_name = error.__class__.__name__
            if skip_retry is True:
                break

            if isinstance(error, RetryAfter):
                sleep_time = error.retry_after + randint(1, 3)
            elif isinstance(error, TimedOut):
                sleep_time = 5

            if need_response is False:
                logger.warning(
                    f"{error_name}{i}({sleep_time}): "
                    f'creating JOB "{function.__name__}" '
                )
                job_name = (
                    f"{function_caller}->"
                    "CALL_TELEGRAM_MESSAGE_FUNCTION->"
                    f"JOB_CALL_TELEGRAM-{ObjectId()}"
                )
                context.job_queue.run_once(
                    callback=job_call_telegram,
                    when=timedelta(seconds=sleep_time),
                    data=job_call_telegram_kwargs,
                    name=job_name,
                    job_kwargs=BASE_JOB_KWARGS,
                )
                return ConversationHandler.END

            logger.warning(
                f'{error_name}{i}: RETRYING activate "{function.__name__}" '
                f"from {function_caller} in {sleep_time} seconds."
            )
            sleep(sleep_time)
            continue

    if is_error is True:
        logger.warning(f"ERROR: {function_caller}")
        if catched_error:
            raise catched_error
        raise Exception(f"Error in {function_caller}")

    if (
        isinstance(response, Message)
        and is_chat_group(message=response)
        and auto_delete_message
    ):
        complete_function_caller = (
            f"{function_caller}->" "CALL_TELEGRAM_MESSAGE_FUNCTION()"
        )
        schedule_job_delete_message_from_context(
            function_caller=complete_function_caller,
            context=context,
            message=response,
            when=auto_delete_message,
        )

    return response


async def send_message_text(
    function_caller: str,
    text: str,
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: Optional[int] = None,
    user_id: Optional[int] = None,
    markdown: bool = False,
    silent: Optional[bool] = None,
    reply_markup: InlineKeyboardMarkup = REPLY_MARKUP_DEFAULT,
    allow_sending_without_reply: bool = True,
    close_by_owner: bool = True,
    need_response: bool = False,
    skip_retry: bool = False,
    auto_delete_message: Union[bool, int, timedelta] = True,
) -> Message:
    """Envia uma mensagem.

    Se markdown for True, o parse_mode será igual a
    ParseMode.MARKDOWN_V2, caso contrário, parse_mode será igual a None

    Se silent for None, usará a configuração de notificação do chat em
    disable_notification.

    Se reply_markup não for passado, a mensagem terá um botão de fechar.

    Se close_by_owner for True e não for passado reply_markup, a mensagem terá
    um botão de fechar que somente o usuário responsável pelo envio da
    mensagem que poderá fechá-la. Caso contrário,
    qualquer jogador poderá fechar.
    """

    chat_id = chat_id if chat_id else context._chat_id
    user_id = user_id if user_id else context._user_id
    markdown = ParseMode.MARKDOWN_V2 if markdown is True else None
    owner_id = user_id if close_by_owner is True else None
    reply_markup = (
        reply_markup
        if reply_markup != REPLY_MARKUP_DEFAULT
        else get_close_keyboard(user_id=owner_id)
    )

    # TODO implementar atributo `silence` em Player e na class que for
    # representar o grupo
    # if silent is None:
    #     if isinstance(chat_id, int):
    #         silent = get_attribute_group_or_player(chat_id, "silent")
    #     elif isinstance(user_id, int):
    #         silent = get_player_attribute_by_id(user_id, "silent")

    send_text_kwargs = dict(
        chat_id=chat_id,
        text=text,
        parse_mode=markdown,
        disable_notification=silent,
        reply_markup=reply_markup,
    )

    response = await call_telegram_message_function(
        function_caller=function_caller,
        function=context.bot.send_message,
        context=context,
        need_response=need_response,
        skip_retry=skip_retry,
        auto_delete_message=auto_delete_message,
        **send_text_kwargs,
    )

    return response


async def edit_message_text(
    function_caller: str,
    text: str,
    context: ContextTypes.DEFAULT_TYPE,
    update: Optional[Update] = None,
    chat_id: Optional[int] = None,
    user_id: Optional[int] = None,
    message_id: Optional[int] = None,
    markdown: bool = False,
    reply_markup: InlineKeyboardMarkup = REPLY_MARKUP_DEFAULT,
    close_by_owner: bool = True,
    need_response: bool = True,
    skip_retry: bool = False,
) -> Union[Message, bool]:
    """Edita uma mensagem usando um Message ou um ContextTypes."""

    if update and not message_id:
        message_id = update.effective_message.id
    if message_id is None:
        raise ValueError("É obrigatório passar o update ou o message_id.")

    chat_id = chat_id if chat_id else context._chat_id
    user_id = user_id if user_id else context._user_id
    markdown = ParseMode.MARKDOWN_V2 if markdown is True else None
    owner_id = user_id if close_by_owner is True else None
    reply_markup = (
        reply_markup
        if reply_markup != REPLY_MARKUP_DEFAULT
        else get_close_keyboard(user_id=owner_id)
    )
    edit_text_kwargs = dict(
        text=text,
        chat_id=chat_id,
        message_id=message_id,
        parse_mode=markdown,
        reply_markup=reply_markup,
    )

    response = await call_telegram_message_function(
        function_caller=f"{function_caller} -> EDIT_MESSAGE_EDIT()",
        function=context.bot.edit_message_text,
        context=context,
        need_response=need_response,
        skip_retry=skip_retry,
        **edit_text_kwargs,
    )

    return response


async def delete_message_from_context(
    function_caller: str,
    context: ContextTypes.DEFAULT_TYPE,
    message_id: int,
):
    """Deleta a mensagem usando context, mas ignora ação caso
    ocorra um erro BadRequest (Mensagem não encontrada).
    """

    chat_id = context._chat_id
    function_caller = f"{function_caller}->DELETE_MESSAGE_FROM_CONTEXT()"
    try:
        logger.info("DELETE_MESSAGE_FROM_CONTEXT() TRYING DELETE_MESSAGE")
        delete_message_kwargs = dict(chat_id=chat_id, message_id=message_id)
        await call_telegram_message_function(
            function_caller=function_caller,
            function=context.bot.delete_message,
            context=context,
            need_response=False,
            auto_delete_message=False,
            **delete_message_kwargs,
        )
    except BadRequest as e:
        logger.warning("DELETE_MESSAGE_FROM_CONTEXT() BADREQUEST EXCEPT")
        if "Message to delete not found" in e.message:
            logger.warning(f'\tError Message: "{e.message}"')
        elif "Message can't be deleted" in e.message:
            logger.warning(f'\tError Message: "{e.message}" (Sem Permissão)')
        else:
            raise e


async def reply_message(
    function_caller: str,
    text: str,
    context: ContextTypes.DEFAULT_TYPE,
    update: Optional[Update] = None,
    chat_id: Optional[int] = None,
    user_id: Optional[int] = None,
    message_id: Optional[int] = None,
    markdown: bool = False,
    silent: Optional[bool] = None,
    reply_markup: InlineKeyboardMarkup = REPLY_MARKUP_DEFAULT,
    allow_sending_without_reply: bool = True,
    close_by_owner: bool = True,
    need_response: bool = False,
    skip_retry: bool = False,
    auto_delete_message: Union[bool, int, timedelta] = True,
) -> Message:
    """Responde uma mensagem.

    É obrigatório passar update ou message_id.

    Se markdown for True, o parse_mode será igual a
    ParseMode.MARKDOWN_V2, caso contrário, parse_mode será igual a None

    Se silent for None, usará a configuração de notificação do chat em
    disable_notification.

    Se reply_markup não for passado, a mensagem terá um botão de fechar.

    Se close_by_owner for True e não for passado reply_markup, a mensagem terá
    um botão de fechar que somente o usuário responsável pelo envio da
    mensagem que poderá fechá-la. Caso contrário,
    qualquer jogador poderá fechar.
    """

    if update and not message_id:
        message_id = update.effective_message.id
    if message_id is None:
        raise ValueError("É obrigatório passar o update ou o message_id.")

    chat_id = chat_id if chat_id else context._chat_id
    user_id = user_id if user_id else context._user_id
    markdown = ParseMode.MARKDOWN_V2 if markdown is True else None
    reply_parameters = ReplyParameters(
        message_id=message_id,
        allow_sending_without_reply=allow_sending_without_reply,
    )
    owner_id = user_id if close_by_owner is True else None
    reply_markup = (
        reply_markup
        if reply_markup != REPLY_MARKUP_DEFAULT
        else get_close_keyboard(user_id=owner_id)
    )

    # TODO implementar atributo `silence` em Player e na class que for
    # representar o grupo
    # if silent is None:
    #     if isinstance(chat_id, int):
    #         silent = get_attribute_group_or_player(chat_id, "silent")
    #     elif isinstance(user_id, int):
    #         silent = get_player_attribute_by_id(user_id, "silent")

    reply_text_kwargs = dict(
        chat_id=chat_id,
        text=text,
        parse_mode=markdown,
        disable_notification=silent,
        reply_markup=reply_markup,
        reply_parameters=reply_parameters,
    )

    response = await call_telegram_message_function(
        function_caller=function_caller,
        function=context.bot.send_message,
        context=context,
        need_response=need_response,
        skip_retry=skip_retry,
        auto_delete_message=auto_delete_message,
        **reply_text_kwargs,
    )

    return response


# CALL IMAGE TELEGRAM FUNCTIONs ==============================================

# QUERY FUNCTIONS ============================================================
async def delete_message_from_query(
    function_caller: str,
    context: ContextTypes.DEFAULT_TYPE,
    query: CallbackQuery,
):
    """Deleta a mensagem usando query,
    caso ocorra um erro BadRequest tenta deletar a mensagem usando o context.
    """

    message_id = query.message.message_id
    try:
        logger.info("DELETE_MESSAGE() TRYING QUERY.DELETE_MESSAGE")
        await call_telegram_message_function(
            function_caller=function_caller + " and DELETE_MESSAGE()",
            function=query.delete_message,
            context=context,
            auto_delete_message=False,
        )
    except BadRequest as e:
        logger.warning("DELETE_MESSAGE() BADREQUEST EXCEPT")
        if "Query is too old" in e.message:
            await delete_message_from_context(
                function_caller=function_caller,
                context=context,
                message_id=message_id,
            )
        elif "Message to delete not found" in e.message:
            logger.warning(f'\tError Message: "{e.message}"')
        else:
            raise e


async def answer(query: CallbackQuery, text: str, **kwargs):
    """Tenta enviar um answer, caso ocorra um erro, print o erro e o text"""

    try:
        await query.answer(text=text, **kwargs)
    except BadRequest:
        logger.warning("ANSWER() BADREQUEST EXCEPT.")
        logger.warning(f"  text: {text}")


# CALLBACK FUNCTIONS =========================================================
def dict_to_callback_data(callback_dict: dict) -> str:
    """Transforma um dicionário em uma string compactada usada no campo data
    de um botão.
    """

    items = []
    for key, value in callback_dict.items():
        key_int = CALLBACK_KEY_LIST.index(key)
        if isinstance(value, (str, ObjectId)):
            items.append(f'{key_int}:"{value}"')
        else:
            items.append(f"{key_int}:{value}")
    text = ",".join(items)
    text = f"{text}"

    return text


def callback_data_to_dict(callback_data: str) -> dict:
    """Transforma de volta uma string compactada usada no campo data
    de um botão em um dicionário.
    """

    if not callback_data.startswith("{"):
        callback_data = "{" + callback_data
    if not callback_data.endswith("}"):
        callback_data = callback_data + "}"

    callback_data = eval(callback_data)
    callback_data = {
        CALLBACK_KEY_LIST[key]: value for key, value in callback_data.items()
    }
    return callback_data


# JOB FUNCTIONs ==============================================================
# Funções usandas no callback de agendamentos do context.job_queue
async def job_call_telegram(context: ContextTypes.DEFAULT_TYPE):
    """Job que chama a função call_telegram_message_function caso ocorra um
    erro do tipo RetryAfter, TimedOut e o need_response seja False
    """

    logger.info("JOB_CALL_TELEGRAM()")
    job = context.job
    call_telegram_kwargs = job.data
    call_telegram_kwargs["function_caller"] += " and JOB_CALL_TELEGRAM()"
    logger.info(call_telegram_kwargs["function_caller"])

    await call_telegram_message_function(**call_telegram_kwargs)


async def job_delete_message_from_context(context: ContextTypes.DEFAULT_TYPE):
    """Job que exclui a mensagem após um tempo pré determinado."""

    logger.info("JOB_DELETE_MESSAGE_FROM_CONTEXT()")
    job = context.job
    data = job.data
    message_id = data["message_id"]
    function_caller = data["function_caller"]

    await delete_message_from_context(
        function_caller=function_caller, context=context, message_id=message_id
    )


# SCHEDULE JOB FUNCTIONs =====================================================
def schedule_job_delete_message_from_context(
    function_caller: str,
    context: ContextTypes.DEFAULT_TYPE,
    message: Message,
    when: Union[bool, int, timedelta] = True,
):
    """Cria o job que excluirá a mensagem após o tempo passado em `when`."""

    chat_id = message.chat_id
    message_id = message.message_id
    job_name = get_job_delete_message_from_context_name(
        chat_id=chat_id, message_id=message_id
    )
    data = {
        "message_id": message_id,
        "function_caller": function_caller,
    }
    when = get_hours_delete_message_from_context(value=when)
    if not job_exists(context=context, job_name=job_name):
        context.job_queue.run_once(
            callback=job_delete_message_from_context,
            when=when,
            data=data,
            name=job_name,
            chat_id=chat_id,
            job_kwargs=BASE_JOB_KWARGS,
        )
        logger.info(
            f"Mensagem de ID {message_id} do chat de ID {chat_id} "
            f"será excluida em {when}."
        )
    else:
        logger.info(f'Job "{job_name}" já existe.')


def remove_job_delete_message_from_context(
    context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_id: int
):
    job_name = get_job_delete_message_from_context_name(
        chat_id=chat_id, message_id=message_id
    )
    remove_job_by_name(context=context, job_name=job_name)


# SUPPORT FUNCTIONs ==========================================================
def get_hours_delete_message_from_context(
    chat_id: Optional[int] = None,
    value: Union[bool, int, timedelta] = HOURS_DELETE_MESSAGE_FROM_CONTEXT,
) -> timedelta:
    """Retorna o tempo para deletar uma mensagem após um tempo
    pré determinado.
    """

    raw_value = value
    if value is True:
        value = HOURS_DELETE_MESSAGE_FROM_CONTEXT
    if isinstance(value, int) and value > 0:
        value = get_timedelta_from_chat(chat_id=chat_id, hours=value)
    if isinstance(value, timedelta):
        return value
    else:
        raise TypeError(
            "value precisa ser do tipo "
            f'"bool", "int" ou "timedelta" ({type(raw_value)}). '
            'Caso seja do tipo "bool", deve ser True. '
            f'Caso seja do tipo "int", deve ser maior que zero ({raw_value}).'
        )


def get_timedelta_from_chat(
    chat_id: Optional[int] = None, minutes: int = 0, hours: int = 0
) -> timedelta:
    if minutes < 0 or hours < 0:
        raise ValueError(
            "Os valores de tempo (minutes e hours) "
            "não podem ser menores que zero. "
            f"minutes={minutes} e hours={hours}."
        )
    elif minutes == hours == 0:
        raise ValueError(
            "minutes e hours não podem ser igual zero simultâneamente."
        )

    time_multiplier = 1
    if isinstance(chat_id, int):
        # TODO alterar `time_multiplier` para o valor do grupo
        ...

    kwargs = dict(
        minutes=minutes * time_multiplier,
        hours=hours * time_multiplier,
    )

    return timedelta(**kwargs)


def get_job_delete_message_from_context_name(chat_id, message_id):
    return f"DELETE_MESSAGE_FROM_CONTEXT_{chat_id}_{message_id}"


def is_chat_group(
    message: Optional[Message] = None, chat_type: Optional[str] = None
) -> bool:
    if isinstance(message, Message):
        chat_type = message.chat.type
    elif not isinstance(chat_type, str):
        raise TypeError(
            f'message precisa ser do tipo "Message" ({type(message)}) ou '
            f'chat_type precisa ser do tipo "str" ({type(chat_type)}).'
        )

    return chat_type in CHAT_TYPE_GROUPS


def remove_job_by_name(
    context: ContextTypes.DEFAULT_TYPE, job_name: str
) -> bool:
    """Remove o job pelo nome."""

    current_jobs = context.job_queue.get_jobs_by_name(job_name)
    logger.info(f"CURRENT_JOBS: {current_jobs}")
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
        logger.info(f"JOB REMOVIDO: {job.name}")

    return True


def job_exists(context: ContextTypes.DEFAULT_TYPE, job_name: str) -> bool:
    """Verifica se o job existe.
    Retorna True se o job existir, False caso contrário.
    """

    current_jobs = context.job_queue.get_jobs_by_name(job_name)

    return bool(current_jobs)


# BUTTONS FUNCTIONS ==========================================================
def get_button(
    user_id: int,
    text: str,
    command: str,
    left_button_text: str,
    right_button_text: str,
    right_icon: bool = False,
) -> InlineKeyboardButton:
    """ """

    if text is None:
        text = left_button_text
        if right_icon:
            text = right_button_text

    callback_data = dict_to_callback_data(
        {"command": command, "user_id": user_id}
    )
    button = InlineKeyboardButton(text=text, callback_data=callback_data)

    return button


def get_close_button(
    user_id: int,
    text: Optional[str] = None,
    right_icon: bool = False,
) -> InlineKeyboardButton:
    """Se user_id for None, qualquer um pode fechar a mensagem,
    caso contrário, somente o usuário com o mesmo user_id poderar fechar
    a mensagem.
    """

    close_button = get_button(
        user_id=user_id,
        text=text,
        command=CALLBACK_COMMAND_CLOSE,
        left_button_text=LEFT_CLOSE_BUTTON_TEXT,
        right_button_text=RIGHT_CLOSE_BUTTON_TEXT,
        right_icon=right_icon,
    )

    return close_button


def get_refresh_button(
    user_id: int,
    command: str,
    text: Optional[str] = None,
    right_icon: bool = False,
) -> InlineKeyboardButton:
    """Se user_id for None, qualquer um pode recarregar a mensagem,
    caso contrário, somente o usuário com o mesmo user_id poderar recarregar
    a mensagem.
    """

    refresh_button = get_button(
        user_id=user_id,
        text=text,
        command=command,
        left_button_text=LEFT_REFRESH_BUTTON_TEXT,
        right_button_text=RIGHT_REFRESH_BUTTON_TEXT,
        right_icon=right_icon,
    )

    return refresh_button


def get_update_button(
    user_id: int,
    command: str,
    text: Optional[str] = None,
    right_icon: bool = False,
) -> InlineKeyboardButton:
    """Se user_id for None, qualquer um pode atualizar a mensagem,
    caso contrário, somente o usuário com o mesmo user_id poderar atualizar
    a mensagem.
    """

    update_button = get_button(
        user_id=user_id,
        text=text,
        command=command,
        left_button_text=LEFT_UPDATE_BUTTON_TEXT,
        right_button_text=RIGHT_UPDATE_BUTTON_TEXT,
        right_icon=right_icon,
    )

    return update_button


# KEYBOARDS FUNCTIONS ========================================================
def get_close_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Se user_id for None, qualquer um pode fechar a mensagem,
    caso contrário, somente o usuário com o mesmo user_id poderar fechar
    a mensagem.
    """

    close_button = get_close_button(user_id=user_id)
    return InlineKeyboardMarkup([[close_button]])


def get_refresh_close_keyboard(
    user_id: int,
    refresh_command: str,
    refresh_text: Optional[str] = None,
) -> InlineKeyboardMarkup:
    """Se user_id for None, qualquer um pode recarregar e fechar a mensagem,
    caso contrário, somente o usuário com o mesmo user_id poderar recarregar
    e fechar a mensagem.
    """

    refresh_button = get_refresh_button(
        user_id=user_id, command=refresh_command, text=refresh_text
    )
    close_button = get_close_button(user_id=user_id, right_icon=True)
    return InlineKeyboardMarkup([[refresh_button, close_button]])


def get_refresh_update_close_keyboard(
    user_id: int,
    refresh_command: str,
    update_command: str,
    refresh_text: Optional[str] = None,
    update_text: Optional[str] = None,
) -> InlineKeyboardMarkup:
    """Se user_id for None, qualquer um pode recarregar, atualizar e fechar
    a mensagem, caso contrário, somente o usuário com o mesmo user_id poderar
    recarregar, atualizar e fechar a mensagem.
    """

    refresh_button = get_refresh_button(
        user_id=user_id, command=refresh_command, text=refresh_text
    )
    update_button = get_update_button(
        user_id=user_id, command=update_command, text=update_text
    )
    close_button = get_close_button(user_id=user_id, right_icon=True)
    return InlineKeyboardMarkup(
        [[refresh_button, update_button, close_button]]
    )


if __name__ == "__main__":
    callback_dict = {"command": "test", "user_id": 123456789}
    callback_data = dict_to_callback_data(callback_dict)
    print(callback_data)
    print(callback_data_to_dict(callback_data))
