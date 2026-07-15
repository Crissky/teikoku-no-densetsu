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
    alternative_id: str = property(lambda self: AltIdEnum.PLAYER.value)
    save_fields: dict = property(
        lambda self: {
            "owner": {SaveFieldEnum.ATTRIBUTES: ["_id"]},
        }
    )
    populate_fields: dict = property(
        lambda self: {"owner": {PopulateFieldEnum.INITIATOR: PlayerModel}}
    )
