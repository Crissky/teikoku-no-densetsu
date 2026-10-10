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
from repository.mongo.utils.field import QueryField
from repository.mongo.utils.query import Query
from teikoku.entity.register.player import Player

ADMIN_TYPES = (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
PLAYER_ENTITY_TYPE = Player
PLAYER_KEY_VALUE_TYPE = int
PLAYER_KEY_FIELD_ENUM = AltIdEnum.PLAYER
PLAYER_UPDATE_KEY_FIELD_ENUM = UpdateAltIdEnum.PLAYER
PLAYER_CONTEXT_KEY_FIELD_ENUM = ContextAltIdEnum.PLAYER

MODEL = PlayerModel()
logger = logging.getLogger(__name__)


def get_player(
    update: Optional[Update] = None,
    context: Optional[CallbackContext] = None,
) -> Player:
    """Recupera um player a partir de um Update ou CallbackContext do Telegram.

    Extrai o user_id do objeto Update ou CallbackContext fornecido e busca
    o player correspondente no banco de dados.
    """

    query = create_player_query()
    return get_entity(
        model=MODEL,
        query=query,
        update=update,
        context=context,
    )


def get_player_by_user_id(user_id: int) -> Player:
    """Recupera um player do banco de dados pelo ID do usuário."""

    query = create_player_query(user_id=user_id)
    return get_entity_by_alt_id(model=MODEL, query=query)


def save_player(player: Player) -> Player:
    """Salva um player no banco de dados e retorna o player recuperado."""

    query = create_player_query()
    return save_entity(
        entity=player,
        entity_type=PLAYER_ENTITY_TYPE,
        model=MODEL,
        query=query,
    )


def update_player(
    args: Iterable[Tuple[str, Any]],
    player: Optional[Player] = None,
    update: Optional[Update] = None,
) -> Optional[Player]:
    """Atualiza os atributos do player com os valores passados em args.
    args deve ser um iterável de tuplas no formato (atributo, valor).
    """

    query = create_player_query()
    return update_entity(
        args=args,
        entity_type=PLAYER_ENTITY_TYPE,
        model=MODEL,
        query=query,
        entity=player,
        update=update,
    )


def exists_player(
    user_id: Optional[int] = None,
    update: Optional[Update] = None,
    context: Optional[CallbackContext] = None,
) -> bool:
    """Verifica se existe um player no banco de dados."""

    query = create_player_query()
    return exists_entity(
        model=MODEL,
        query=query,
        _id=user_id,
        update=update,
        context=context,
    )


def create_player_query(user_id: int = None):
    query = Query(
        QueryField(
            field=PLAYER_KEY_FIELD_ENUM,
            value=user_id,
            value_type=PLAYER_KEY_VALUE_TYPE,
            field_aliases=(
                PLAYER_UPDATE_KEY_FIELD_ENUM,
                PLAYER_CONTEXT_KEY_FIELD_ENUM,
            ),
        )
    )
    query.check_query_fields()

    return query


async def user_is_admin(update: Update) -> bool:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    chat_member = await update._bot.get_chat_member(
        chat_id=chat_id, user_id=user_id
    )

    return chat_member.status in ADMIN_TYPES
