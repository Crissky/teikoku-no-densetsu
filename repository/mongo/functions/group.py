import logging
from typing import Any, Iterable, Optional, Tuple, get_type_hints

from telegram import Update
from telegram.constants import ChatType
from telegram.ext import CallbackContext

from repository.mongo.enums.field import AltIdEnum
from repository.mongo.functions.entity import save_entity, update_entity
from repository.mongo.models.group import GroupModel
from teikoku.entity.register.group import Group

GROUP_TYPES = (ChatType.GROUP, ChatType.SUPERGROUP)
GROUP_ENTITY_TYPE = Group
GROUP_MODEL_TYPE = GroupModel
GROUP_KEY_VALUE_TYPE = int
GROUP_KEY_FIELD_ENUM = AltIdEnum.GROUP
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
    """Recupera um group do banco de dados pelo ID do chat.

    Args:
        chat_id: ID do chat do Telegram associado ao group.

    Returns:
        Group: Objeto Group correspondente ao chat_id fornecido.

    Raises:
        TypeError: Se chat_id não for do tipo int.
    """

    if not isinstance(chat_id, int):
        raise TypeError(f"chat_id precisa ser um int ({type(chat_id)}).")

    group_model = GroupModel()
    query = {"chat_id": chat_id}
    group = group_model.get(query=query)

    return group


def get_group(
    update: Optional[Update] = None,
    context: Optional[CallbackContext] = None,
) -> Group:
    """Recupera um group a partir de um Update ou CallbackContext do Telegram.

    Extrai o chat_id do objeto Update ou CallbackContext fornecido e busca
    o group correspondente no banco de dados.

    Args:
        update: Objeto Update do Telegram contendo informações da mensagem.
        context: Objeto CallbackContext do Telegram contendo o contexto da
            callback.

    Returns:
        Group: Objeto Group correspondente ao chat_id extraído.

    Raises:
        ValueError: Se nem update nem context forem fornecidos.
    """

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
    context: Optional[CallbackContext] = None,
) -> bool:
    """Verifica se existe um group no banco de dados.

    Pode verificar a existência usando diretamente um chat_id ou extraindo-o
    de um objeto Update ou CallbackContext do Telegram.

    Args:
        chat_id: ID do chat do Telegram a ser verificado.
        update: Objeto Update do Telegram para extrair o chat_id.
        context: Objeto CallbackContext do Telegram para extrair o chat_id.

    Returns:
        bool: True se o group existe, False caso contrário.

    Raises:
        TypeError: Se chat_id não for do tipo int após extração.
    """

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
