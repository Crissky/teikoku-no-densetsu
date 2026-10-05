import logging
from typing import Any, Iterable, Optional, Tuple

from telegram import Update
from telegram.constants import ChatType
from telegram.ext import CallbackContext

from repository.mongo.enums.field import (
    AltIdEnum,
    ContextAltIdEnum,
    UpdateAltIdEnum,
)
from repository.mongo.functions.entity import (
    exists_entity,
    get_entity,
    get_entity_by_alt_id,
    save_entity,
    update_entity,
)
from repository.mongo.models.group import GroupModel
from repository.mongo.utils.field import QueryField
from repository.mongo.utils.query import Query
from teikoku.entity.register.group import Group

GROUP_TYPES = (ChatType.GROUP, ChatType.SUPERGROUP)
GROUP_ENTITY_TYPE = Group
GROUP_MODEL_TYPE = GroupModel
GROUP_KEY_VALUE_TYPE = int
GROUP_KEY_FIELD_ENUM = AltIdEnum.GROUP
GROUP_UPDATE_KEY_FIELD_ENUM = UpdateAltIdEnum.GROUP
GROUP_CONTEXT_KEY_FIELD_ENUM = ContextAltIdEnum.GROUP

MODEL = GroupModel()
logger = logging.getLogger(__name__)


def get_group(
    update: Optional[Update] = None,
    context: Optional[CallbackContext] = None,
) -> Group:
    """Recupera um group a partir de um Update ou CallbackContext do Telegram."""

    query = create_group_query()
    return get_entity(
        model=MODEL,
        query=query,
        update=update,
        context=context,
    )


def get_group_by_chat_id(chat_id: int) -> Group:
    """Recupera um group do banco de dados pelo ID do chat."""

    query = create_group_query(chat_id=chat_id)
    return get_entity_by_alt_id(model=MODEL, query=query)


def save_group(group: Group) -> Group:
    """Salva um group no banco de dados e retorna o group recuperado."""

    query = create_group_query()
    return save_entity(
        entity=group,
        entity_type=GROUP_ENTITY_TYPE,
        model=MODEL,
        query=query,
    )


def update_group(
    args: Iterable[Tuple[str, Any]],
    group: Optional[Group] = None,
    update: Optional[Update] = None,
) -> Optional[Group]:
    """Atualiza os atributos do group com os valores passados em args.
    args deve ser um iterável de tuplas no formato (atributo, valor).
    """

    query = create_group_query()
    return update_entity(
        args=args,
        entity_type=GROUP_ENTITY_TYPE,
        model=MODEL,
        query=query,
        entity=group,
        update=update,
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
        key_value_type=GROUP_KEY_VALUE_TYPE,
        key_value=chat_id,
        update=update,
        context=context,
    )


def chat_is_group(update: Update) -> bool:
    return update.effective_chat.type in GROUP_TYPES


def create_group_query(chat_id: int = None):
    query = Query(
        QueryField(
            field=AltIdEnum.GROUP,
            value=chat_id,
            value_type=int,
            field_aliases=(UpdateAltIdEnum.GROUP, ContextAltIdEnum.GROUP),
        )
    )
    query.check_query_fields()

    return query
