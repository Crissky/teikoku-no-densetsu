import logging

from repository.mongo.collection_enum import CollectionEnum
from repository.mongo.models.model import Model
from teikoku.register.group import Group

logger = logging.getLogger(__name__)


class GroupModel(Model):
    _class = property(lambda self: Group)
    collection = property(lambda self: CollectionEnum.GROUP.value)
    alternative_id: str = property(lambda self: "chat_id")


if __name__ == "__main__":
    print(" START LOCAL TEST ".center(79, "="))
    group = Group(chat_id=123456789, name="Teste")
    group_model = GroupModel()

    print("COLLECTION NAME:")
    print(group_model.collection)

    print("\nSAVING GROUP...")
    group_model.save(group)

    print("\nRETRIEVING SAVED GROUP...")
    retrieved_group = group_model.get(123456789)
    if retrieved_group is None:
        raise ValueError(f"retrieved_group é None ({retrieved_group}).")
    print("\nRETRIEVED GROUP:")
    print(retrieved_group)
    print("\nEQUALS:", group == retrieved_group)
    if group != retrieved_group:
        raise ValueError(
            "O valor salvo é diferente do valor recuperado.\n"
            f"Valor Salvo: {group}\n"
            f"Valor Recuperado: {retrieved_group}\n"
        )

    print(" END LOCAL TEST ".center(79, "="))
