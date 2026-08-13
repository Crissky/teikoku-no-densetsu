import logging
from typing import Any, Iterable, Optional, Tuple

from telegram import Update
from telegram.constants import ChatMemberStatus
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
from repository.mongo.models.player import PlayerModel
from teikoku.entity.register.player import Player

ADMIN_TYPES = (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
PLAYER_ENTITY_TYPE = Player
PLAYER_MODEL_TYPE = PlayerModel
PLAYER_KEY_VALUE_TYPE = int
PLAYER_KEY_FIELD_ENUM = AltIdEnum.PLAYER
PLAYER_UPDATE_KEY_FIELD_ENUM = UpdateAltIdEnum.PLAYER
PLAYER_CONTEXT_KEY_FIELD_ENUM = ContextAltIdEnum.PLAYER
logger = logging.getLogger(__name__)


def save_player(player: Player) -> Player:
    """Salva um player no banco de dados e retorna o player recuperado."""

    return save_entity(
        entity=player,
        entity_type=PLAYER_ENTITY_TYPE,
        model_type=PLAYER_MODEL_TYPE,
        key_value_type=PLAYER_KEY_VALUE_TYPE,
        key_field_enum=PLAYER_KEY_FIELD_ENUM,
    )


def update_player(
    args: Iterable[Tuple[str, Any]],
    player: Optional[Player] = None,
    update: Optional[Update] = None,
) -> Optional[Player]:
    """Atualiza os atributos do player com os valores passados em args.
    args deve ser um iterável de tuplas no formato (atributo, valor).
    """

    return update_entity(
        args=args,
        entity_type=PLAYER_ENTITY_TYPE,
        model_type=PLAYER_MODEL_TYPE,
        key_value_type=PLAYER_KEY_VALUE_TYPE,
        key_field_enum=PLAYER_KEY_FIELD_ENUM,
        update_key_field_enum=PLAYER_UPDATE_KEY_FIELD_ENUM,
        entity=player,
        update=update,
    )


def get_player_by_user_id(user_id: int) -> Player:
    """Recupera um player do banco de dados pelo ID do usuário."""

    return get_entity_by_alt_id(
        model_type=PLAYER_MODEL_TYPE,
        key_value=user_id,
        key_value_type=PLAYER_KEY_VALUE_TYPE,
        key_field_enum=PLAYER_KEY_FIELD_ENUM,
    )


def get_player(
    update: Optional[Update] = None,
    context: Optional[CallbackContext] = None,
) -> Player:
    """Recupera um player a partir de um Update ou CallbackContext do Telegram.

    Extrai o user_id do objeto Update ou CallbackContext fornecido e busca
    o player correspondente no banco de dados.
    """

    return get_entity(
        model_type=PLAYER_MODEL_TYPE,
        key_value_type=PLAYER_KEY_VALUE_TYPE,
        key_field_enum=PLAYER_KEY_FIELD_ENUM,
        update_key_field_enum=PLAYER_UPDATE_KEY_FIELD_ENUM,
        context_key_field_enum=PLAYER_CONTEXT_KEY_FIELD_ENUM,
        update=update,
        context=context,
    )


def exists_player(
    user_id: Optional[int] = None,
    update: Optional[Update] = None,
    context: Optional[CallbackContext] = None,
) -> bool:
    """Verifica se existe um player no banco de dados."""

    return exists_entity(
        model_type=PLAYER_MODEL_TYPE,
        update_key_field_enum=PLAYER_UPDATE_KEY_FIELD_ENUM,
        context_key_field_enum=PLAYER_CONTEXT_KEY_FIELD_ENUM,
        key_value_type=PLAYER_KEY_VALUE_TYPE,
        key_value=user_id,
        update=update,
        context=context,
    )


async def user_is_admin(update: Update) -> bool:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    chat_member = await update._bot.get_chat_member(
        chat_id=chat_id, user_id=user_id
    )

    return chat_member.status in ADMIN_TYPES
