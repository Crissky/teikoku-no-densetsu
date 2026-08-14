import logging

from typing import Any, Iterable, Optional, Tuple, get_type_hints

from telegram import Update
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
from repository.mongo.models.world import WorldModel
from teikoku.entity.world.world import World

WORLD_ENTITY_TYPE = World
WORLD_MODEL_TYPE = WorldModel
WORLD_KEY_VALUE_TYPE = int
WORLD_KEY_FIELD_ENUM = AltIdEnum.WORLD
WORLD_UPDATE_KEY_FIELD_ENUM = UpdateAltIdEnum.WORLD
WORLD_CONTEXT_KEY_FIELD_ENUM = ContextAltIdEnum.WORLD
logger = logging.getLogger(__name__)


def save_world(world: World) -> World:
    """Salva um world no banco de dados e retorna o world recuperado."""

    return save_entity(
        entity=world,
        entity_type=WORLD_ENTITY_TYPE,
        model_type=WORLD_MODEL_TYPE,
        key_value_type=WORLD_KEY_VALUE_TYPE,
        key_field_enum=WORLD_KEY_FIELD_ENUM,
    )


def update_world(
    args: Iterable[Tuple[str, Any]],
    world: Optional[World] = None,
    update: Optional[Update] = None,
) -> Optional[World]:
    """Atualiza os atributos do world com os valores passados em args.
    args deve ser um iterável de tuplas no formato (atributo, valor).
    """

    return update_entity(
        args=args,
        entity_type=WORLD_ENTITY_TYPE,
        model_type=WORLD_MODEL_TYPE,
        key_value_type=WORLD_KEY_VALUE_TYPE,
        key_field_enum=WORLD_KEY_FIELD_ENUM,
        update_key_field_enum=WORLD_UPDATE_KEY_FIELD_ENUM,
        entity=world,
        update=update,
    )


def get_world_by_chat_id(chat_id: int) -> World:
    """Recupera um world do banco de dados pelo ID do chat."""

    return get_entity_by_alt_id(
        model_type=WORLD_MODEL_TYPE,
        key_value=chat_id,
        key_value_type=WORLD_KEY_VALUE_TYPE,
        key_field_enum=WORLD_KEY_FIELD_ENUM,
    )


def get_world(
    update: Optional[Update] = None,
    context: Optional[CallbackContext] = None,
) -> World:
    """Recupera um world a partir de um Update ou CallbackContext do Telegram.

    Extrai o chat_id do objeto Update ou CallbackContext fornecido e busca
    o world correspondente no banco de dados.
    """

    return get_entity(
        model_type=WORLD_MODEL_TYPE,
        key_value_type=WORLD_KEY_VALUE_TYPE,
        key_field_enum=WORLD_KEY_FIELD_ENUM,
        update_key_field_enum=WORLD_UPDATE_KEY_FIELD_ENUM,
        context_key_field_enum=WORLD_CONTEXT_KEY_FIELD_ENUM,
        update=update,
        context=context,
    )


def exists_world(
    chat_id: Optional[int] = None,
    update: Optional[Update] = None,
    context: Optional[CallbackContext] = None,
) -> bool:
    """Verifica se existe um world no banco de dados."""

    return exists_entity(
        model_type=WORLD_MODEL_TYPE,
        update_key_field_enum=WORLD_UPDATE_KEY_FIELD_ENUM,
        context_key_field_enum=WORLD_CONTEXT_KEY_FIELD_ENUM,
        key_value_type=WORLD_KEY_VALUE_TYPE,
        key_value=chat_id,
        update=update,
        context=context,
    )
