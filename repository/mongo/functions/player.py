import logging

from repository.mongo.models.player import PlayerModel
from teikoku.register.player import Player


logger = logging.getLogger(__name__)


def save_player(player: Player) -> Player:
    if not isinstance(player, Player):
        raise TypeError(f"player precisa ser do tipo Player ({type(player)}).")

    player_model = PlayerModel()
    player_model.save(player)
    saved_player = get_player_by_user_id(player.user_id)
    logger.info(
        f"Player '{saved_player.name}' salvo com "
        f"USER ID '{saved_player.user_id}'"
    )

    return saved_player


def get_player_by_user_id(user_id: int) -> Player:
    if not isinstance(user_id, int):
        raise TypeError("user_id precisa ser uma int.")

    player_model = PlayerModel()
    player = player_model.get(query={"user_id": user_id})

    return player


def exists_player(user_id: int) -> bool:
    if not isinstance(user_id, int):
        raise TypeError("user_id precisa ser uma int.")
    player_model = PlayerModel()

    return player_model.exists(_id=user_id)
