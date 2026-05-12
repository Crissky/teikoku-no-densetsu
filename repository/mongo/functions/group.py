import logging
from typing import Optional

from telegram import Update
from telegram.constants import ChatType
from telegram.ext import CallbackContext, ContextTypes

from repository.mongo.models.group import GroupModel
from teikoku.register.group import Group

GROUP_TYPES = (ChatType.GROUP, ChatType.SUPERGROUP)
logger = logging.getLogger(__name__)


def save_group(group: Group) -> Group:
    if not isinstance(group, Group):
        raise TypeError(f"group precisa ser do tipo Group ({type(group)}).")

    group_model = GroupModel()
    group_model.save(group)
    retrieved_group = get_group_by_chat_id(group.chat_id)
    logger.info(
        f"Group '{retrieved_group.name}' salvo com "
        f"CHAT ID '{retrieved_group.chat_id}'"
    )

    return retrieved_group


def get_group_by_chat_id(chat_id: int) -> Group:
    if not isinstance(chat_id, int):
        raise TypeError("chat_id precisa ser um int.")

    group_model = GroupModel()
    group = group_model.get(query={"chat_id": chat_id})

    return group


def get_group(
    update: Optional[Update] = None,
    context: Optional[ContextTypes.DEFAULT_TYPE] = None,
) -> Group:
    if isinstance(update, Update):
        chat_id = update.effective_chat.id
    elif isinstance(context, CallbackContext):
        chat_id = context._chat_id
    else:
        raise ValueError("É preciso informar ou update ou context.")

    return get_group_by_chat_id(chat_id)


def exists_group(
    chat_id: Optional[int] = None,
    update: Optional[Update] = None,
    context: Optional[ContextTypes.DEFAULT_TYPE] = None,
) -> bool:
    if isinstance(update, Update) and chat_id is None:
        chat_id = update.effective_chat.id
    elif isinstance(context, CallbackContext) and chat_id is None:
        chat_id = context._chat_id
    if not isinstance(chat_id, int):
        raise TypeError("chat_id precisa ser um int.")
    group_model = GroupModel()

    return group_model.exists(_id=chat_id)


def chat_is_group(update: Update) -> bool:
    return update.effective_chat.type in GROUP_TYPES
