import logging
from typing import Any, Iterable, Optional, Tuple, get_type_hints

from telegram import Update
from telegram.constants import ChatMemberStatus
from telegram.ext import CallbackContext, ContextTypes

from repository.mongo.models.player import PlayerModel
from teikoku.entity.register.player import Player

ADMIN_TYPES = (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
logger = logging.getLogger(__name__)


def save_player(player: Player) -> Player:
    if not isinstance(player, Player):
        raise TypeError(f"player precisa ser do tipo Player ({type(player)}).")

    player_model = PlayerModel()
    player_model.save(player)
    retrieved_player = get_player_by_user_id(player.user_id)
    logger.info(
        f"Player '{retrieved_player.name}' salvo com "
        f"USER ID '{retrieved_player.user_id}'"
    )

    return retrieved_player


def update_player(
    args: Iterable[Tuple[str, Any]],
    player: Optional[Player] = None,
    update: Optional[Update] = None,
) -> Optional[Player]:
    """Atualiza os atributos do player com os valores passados em args.
    args deve ser um iterável de tuplas no formato (atributo, valor).
    Exemplo: [("name", "João"), ("username", "@joaozinho")]
    """

    if isinstance(update, Update) and player is None:
        player = get_player(update=update)

    if not isinstance(player, Player):
        raise TypeError(f"player precisa ser do tipo Player ({type(player)}).")

    is_updated = False
    player_type_hints = get_type_hints(player)
    for attr, value in args:
        if player.has_updatable_attr(attr):
            player_attr_type = player_type_hints[attr]
            if player_attr_type == type(value):
                setattr(player, attr, value)
                is_updated = True
            else:
                logger.warning(
                    f"O atributo '{attr}' não pode ser atualizado com o valor "
                    f"do tipo {type(value)}, pois o tipo esperado é "
                    f"{type(player_attr_type)}."
                )
        else:
            logger.warning(
                f"Player não possui ou não pode alterar o atributo '{attr}'."
            )

    if is_updated:
        player_model = PlayerModel()
        player_model.save(player)
        retrieved_player = get_player_by_user_id(player.user_id)

        return retrieved_player


def get_player_by_user_id(user_id: int) -> Player:
    if not isinstance(user_id, int):
        raise TypeError("user_id precisa ser um int.")

    player_model = PlayerModel()
    player = player_model.get(query={"user_id": user_id})

    return player


def get_player(
    update: Optional[Update] = None,
    context: Optional[ContextTypes.DEFAULT_TYPE] = None,
) -> Player:
    if isinstance(update, Update):
        user_id = update.effective_user.id
    elif isinstance(context, CallbackContext):
        user_id = context._user_id
    else:
        raise ValueError("É preciso informar ou update ou context.")

    return get_player_by_user_id(user_id)


def exists_player(
    user_id: Optional[int] = None,
    update: Optional[Update] = None,
    context: Optional[ContextTypes.DEFAULT_TYPE] = None,
) -> bool:
    if isinstance(update, Update) and user_id is None:
        user_id = update.effective_user.id
    elif isinstance(context, CallbackContext) and user_id is None:
        user_id = context._user_id
    if not isinstance(user_id, int):
        raise TypeError("user_id precisa ser um int.")
    player_model = PlayerModel()

    return player_model.exists(_id=user_id)


async def user_is_admin(update: Update) -> bool:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    chat_member = await update._bot.get_chat_member(
        chat_id=chat_id, user_id=user_id
    )

    return chat_member.status in ADMIN_TYPES
