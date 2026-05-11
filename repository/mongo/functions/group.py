import logging

from repository.mongo.models.group import GroupModel
from teikoku.register.group import Group


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


def exists_group(chat_id: int) -> bool:
    if not isinstance(chat_id, int):
        raise TypeError("chat_id precisa ser um int.")
    group_model = GroupModel()

    return group_model.exists(_id=chat_id)
