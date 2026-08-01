import logging
from typing import Any, Iterable, Optional, Tuple, get_type_hints

from telegram import Update
from telegram.constants import ChatType
from telegram.ext import CallbackContext

from repository.mongo.enums.field import AltIdEnum, ContextAltIdEnum, UpdateAltIdEnum
from repository.mongo.functions.entity import exists_entity, get_entity, get_entity_by_alt_id, save_entity, update_entity
from repository.mongo.models.group import GroupModel
from teikoku.entity.register.group import Group

GROUP_TYPES = (ChatType.GROUP, ChatType.SUPERGROUP)
GROUP_ENTITY_TYPE = Group
GROUP_MODEL_TYPE = GroupModel
GROUP_KEY_VALUE_TYPE = int
GROUP_KEY_FIELD_ENUM = AltIdEnum.GROUP
GROUP_UPDATE_KEY_FIELD_ENUM = UpdateAltIdEnum.GROUP
GROUP_CONTEXT_KEY_FIELD_ENUM = ContextAltIdEnum.GROUP
logger = logging.getLogger(__name__)


def save_group(group: Group) -> Group:
    """Salva um group no banco de dados e retorna o group recuperado."""

    return save_entity(
        entity=group,
        entity_type=GROUP_ENTITY_TYPE,
        model_type=GROUP_MODEL_TYPE,
        key_value_type=GROUP_KEY_VALUE_TYPE,
        key_field_enum=GROUP_KEY_FIELD_ENUM,
    )


def update_group(
    args: Iterable[Tuple[str, Any]],
    group: Optional[Group] = None,
    update: Optional[Update] = None,
) -> Optional[Group]:
    """Atualiza os atributos do group com os valores passados em args.
    args deve ser um iterável de tuplas no formato (atributo, valor).
    """

    return update_entity(
        args=args,
        entity_type=GROUP_ENTITY_TYPE,
        model_type=GROUP_MODEL_TYPE,
        key_value_type=GROUP_KEY_VALUE_TYPE,
        key_field_enum=GROUP_KEY_FIELD_ENUM,
        entity=group,
        update=update,
    )


def get_group_by_chat_id(chat_id: int) -> Group:
    """Recupera um group do banco de dados pelo ID do chat."""

    return get_entity_by_alt_id(
        model_type=GROUP_MODEL_TYPE,
        key_value=chat_id,
        key_value_type=GROUP_KEY_VALUE_TYPE,
        key_field_enum=GROUP_KEY_FIELD_ENUM,
    )


def get_group(
    update: Optional[Update] = None,
    context: Optional[CallbackContext] = None,
) -> Group:
    """Recupera um group a partir de um Update ou CallbackContext do Telegram.
    """

    return get_entity(
        model_type=GROUP_MODEL_TYPE,
        key_value_type=GROUP_KEY_VALUE_TYPE,
        key_field_enum=GROUP_KEY_FIELD_ENUM,
        update_key_field_enum=GROUP_UPDATE_KEY_FIELD_ENUM,
        context_key_field_enum=GROUP_CONTEXT_KEY_FIELD_ENUM,
        update=update,
        context=context,
    )


def exists_group(
    chat_id: Optional[int] = None,
    update: Optional[Update] = None,
    context: Optional[CallbackContext] = None,
) -> bool:
    """Verifica se existe um group no banco de dados."""

    return exists_entity(
        model_type=GROUP_MODEL_TYPE,
        update_key_field_enum=GROUP_UPDATE_KEY_FIELD_ENUM,
        context_key_field_enum=GROUP_CONTEXT_KEY_FIELD_ENUM,
        key_value=chat_id,
        update=update,
        context=context,
    )


def chat_is_group(update: Update) -> bool:
    return update.effective_chat.type in GROUP_TYPES
