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
from repository.mongo.models.city import CityModel
from teikoku.entity.city.city_base import City

CITY_ENTITY_TYPE = City
CITY_MODEL_TYPE = CityModel
CITY_KEY_VALUE_TYPE = int
CITY_KEY_FIELD_ENUM = AltIdEnum.CITY
CITY_UPDATE_KEY_FIELD_ENUM = UpdateAltIdEnum.CITY
CITY_CONTEXT_KEY_FIELD_ENUM = ContextAltIdEnum.CITY
logger = logging.getLogger(__name__)


def save_city(city: City) -> City:
    """Salva um city no banco de dados e retorna o city recuperado."""

    return save_entity(
        entity=city,
        entity_type=CITY_ENTITY_TYPE,
        model_type=CITY_MODEL_TYPE,
        key_value_type=CITY_KEY_VALUE_TYPE,
        key_field_enum=CITY_KEY_FIELD_ENUM,
    )


def update_city(
    args: Iterable[Tuple[str, Any]],
    city: Optional[City] = None,
    update: Optional[Update] = None,
) -> Optional[City]:
    """Atualiza os atributos do city com os valores passados em args.
    args deve ser um iterável de tuplas no formato (atributo, valor).
    """

    return update_entity(
        args=args,
        entity_type=CITY_ENTITY_TYPE,
        model_type=CITY_MODEL_TYPE,
        key_value_type=CITY_KEY_VALUE_TYPE,
        key_field_enum=CITY_KEY_FIELD_ENUM,
        update_key_field_enum=CITY_UPDATE_KEY_FIELD_ENUM,
        entity=city,
        update=update,
    )


def get_city_by_chat_id(chat_id: int) -> City:
    """Recupera um city do banco de dados pelo ID do chat."""

    return get_entity_by_alt_id(
        model_type=CITY_MODEL_TYPE,
        key_value=chat_id,
        key_value_type=CITY_KEY_VALUE_TYPE,
        key_field_enum=CITY_KEY_FIELD_ENUM,
    )


def get_city(
    update: Optional[Update] = None,
    context: Optional[CallbackContext] = None,
) -> City:
    """Recupera um city a partir de um Update ou CallbackContext do Telegram.

    Extrai o chat_id do objeto Update ou CallbackContext fornecido e busca
    o city correspondente no banco de dados.
    """

    return get_entity(
        model_type=CITY_MODEL_TYPE,
        key_value_type=CITY_KEY_VALUE_TYPE,
        key_field_enum=CITY_KEY_FIELD_ENUM,
        update_key_field_enum=CITY_UPDATE_KEY_FIELD_ENUM,
        context_key_field_enum=CITY_CONTEXT_KEY_FIELD_ENUM,
        update=update,
        context=context,
    )


def exists_city(
    chat_id: Optional[int] = None,
    update: Optional[Update] = None,
    context: Optional[CallbackContext] = None,
) -> bool:
    """Verifica se existe um city no banco de dados."""

    return exists_entity(
        model_type=CITY_MODEL_TYPE,
        update_key_field_enum=CITY_UPDATE_KEY_FIELD_ENUM,
        context_key_field_enum=CITY_CONTEXT_KEY_FIELD_ENUM,
        key_value_type=CITY_KEY_VALUE_TYPE,
        key_value=chat_id,
        update=update,
        context=context,
    )
