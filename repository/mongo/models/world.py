import logging

from repository.mongo.collection_enum import CollectionEnum
from repository.mongo.models.model import Model
from teikoku.entity.world.world import World

logger = logging.getLogger(__name__)


class WorldModel(Model):
    _class = property(lambda self: World)
    collection = property(lambda self: CollectionEnum.WORLD.value)
    alternative_id: str = property(lambda self: "chat_id")

if __name__ == "__main__":
    print(" START LOCAL TEST ".center(79, "="))
    world = World(name="TESTE WORLD", chat_id=123456789)
    world_model = WorldModel()

    print("COLLECTION NAME:")
    print(world_model.collection)

    print("\nSAVING WORLD...")
    world_model.save(world)

    print("\nRETRIEVING SAVED WORLD...")
    retrieved_world = world_model.get(123456789)
    if retrieved_world is None:
        raise ValueError(f"retrieved_world é None ({retrieved_world}).")
    print("\nRETRIEVED WORLD:")
    print(retrieved_world)
    print("\nEQUALS:", world._id == retrieved_world._id)
    if world._id != retrieved_world._id:
        raise ValueError(
            "O valor salvo é diferente do valor recuperado.\n"
            f"Valor Salvo: {world}\n"
            f"Valor Recuperado: {retrieved_world}\n"
        )

    print(" END LOCAL TEST ".center(79, "="))