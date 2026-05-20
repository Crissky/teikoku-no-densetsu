import logging

from repository.mongo.collection_enum import CollectionEnum
from repository.mongo.models.model import Model
from teikoku.entity.register.player import Player

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

    print("\nRETRIEVING SAVED PLAYER...")
    retrieved_player = player_model.get(123456789)
    if retrieved_player is None:
        raise ValueError(f"retrieved_player é None ({retrieved_player}).")
    print("\nRETRIEVED PLAYER:")
    print(retrieved_player)
    print("\nEQUALS:", player == retrieved_player)
    if player != retrieved_player:
        raise ValueError(
            "O valor salvo é diferente do valor recuperado.\n"
            f"Valor Salvo: {player}\n"
            f"Valor Recuperado: {retrieved_player}\n"
        )

    print(" END LOCAL TEST ".center(79, "="))
