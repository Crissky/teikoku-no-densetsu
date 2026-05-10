import logging

from repository.mongo.collection_enum import CollectionEnum
from repository.mongo.models.model import Model
from teikoku.register.player import Player

logger = logging.getLogger(__name__)


class PlayerModel(Model):
    _class = property(lambda self: Player)
    collection = property(lambda self: CollectionEnum.PLAYER.value)
    alternative_id: str = property(lambda self: "user_id")


if __name__ == "__main__":
    print(" START LOCAL TEST ".center(79, "="))
    player = Player(user_id=123456789, name="Teste")
    player_model = PlayerModel()

    print("COLLECTION NAME:")
    print(player_model.collection)

    print("\nSAVING PLAYER...")
    player_model.save(player)
    saved_player = player_model.get("123456789")

    print("\nGETTING SAVED PLAYER...")
    print("\nSAVED PLAYER:")
    print(saved_player)
    print("\nEQUALS:", player == saved_player)

    print(" END LOCAL TEST ".center(79, "="))
