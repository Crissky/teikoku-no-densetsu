from repository.mongo.enums.collection import CollectionEnum
from repository.mongo.enums.field import (
    AltIdEnum,
    PopulateFieldEnum,
    SaveFieldEnum,
)
from repository.mongo.models.model import Model
from repository.mongo.models.player import PlayerModel
from teikoku.entity.world.city import City


class CityModel(Model):
    _class = property(lambda self: City)
    collection = property(lambda self: CollectionEnum.CITY.value)
    alternative_id: str = property(lambda self: AltIdEnum.CITY.value)
    populate_fields: dict = property(
        lambda self: {
            AltIdEnum.CITY.value: {PopulateFieldEnum.INITIATOR: PlayerModel}
        }
    )


if __name__ == "__main__":
    from teikoku.entity.register.player import Player

    print(" START LOCAL TEST ".center(79, "="))
    player = Player(user_id=987654321, name="Player Teste")
    city = City(
        name="Cidade Teste",
        chat_id=123456789,
        owner=player,
        level=1,
        size=3,
        x=1,
        y=2,
    )
    city_model = CityModel()

    print("COLLECTION NAME:")
    print(city_model.collection)

    print("\nSAVING CITY...")
    city_model.save(city)

    print("\nRETRIEVING SAVED CITY...")
    retrieved_city = city_model.get(987654321)
    if retrieved_city is None:
        raise ValueError(f"retrieved_city é None ({retrieved_city}).")
    print("\nRETRIEVED CITY:")
    print(retrieved_city)
    print("\nEQUALS:", city == retrieved_city)
    if city != retrieved_city:
        raise ValueError(
            "O valor salvo é diferente do valor recuperado.\n"
            f"Valor Salvo: {city}\n"
            f"Valor Recuperado: {retrieved_city}\n"
        )

    print(" END LOCAL TEST ".center(79, "="))
