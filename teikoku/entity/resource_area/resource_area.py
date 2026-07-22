from dataclasses import InitVar, dataclass
from typing import Union

from bson import ObjectId

from repository.mongo.base import MongoBase
from teikoku.enum.resource import (
    CollectibleResourceEnum,
    LocationResourceTypeEnum,
)
from teikoku.util.coor import Coordinate


@dataclass
class ResourceArea(MongoBase):
    quantity: int
    resource: CollectibleResourceEnum
    x: InitVar[int]
    y: InitVar[int]
    location_type: LocationResourceTypeEnum = LocationResourceTypeEnum.MINE
    level: int = 1

    UPDATABLE_ATTR_LIST = ()

    def __post_init__(self, x: int, y: int):

        # QUANTITY
        if self.quantity < 0:
            raise ValueError(
                "O atributo resource precisa ser um valor positivo "
                f"({self.quantity})."
            )

        # RESOURCE
        if isinstance(self.resource, str):
            self.resource = CollectibleResourceEnum[self.resource]

        # COORDINATE
        if isinstance(x, int) and isinstance(y, int):
            self.coor = Coordinate(x=x, y=y)
        else:
            raise TypeError(
                "Os atributos x e y precisam ser do tipo int."
                f"x: {type(self.x)} | y: {type(self.y)}"
            )

        # LOCATION
        if isinstance(self.location_type, str):
            self.location_type = LocationResourceTypeEnum[self.location_type]

        # LEVEL
        if self.level < 0:
            raise ValueError(
                "O atributo level precisa ser um valor positivo "
                f"({self.level})."
            )

        super().__post_init__()

    @property
    def name(self):
        return (
            f"{self.location_type.value.title()} de "
            f"{self.resource.value.title()}"
        )

    @property
    def telegram_text(self):
        resource_name = self.resource.value.title()
        text = f"*Local*: {self.name}\n"
        text += f"*Nível*: {self.level}\n"
        text += f"*{resource_name}*: {self.quantity}\n"

        return text

    @property
    def persisted_fields(self) -> Union[dict, ObjectId]:
        return self.to_dict()

    @property
    def extra_attr(self) -> dict:
        return {
            "x": self.coor.x,
            "y": self.coor.y,
        }


if __name__ == "__main__":
    print(" START LOCAL TEST ".center(79, "="))

    mine = ResourceArea(100, "METAL", x=1, y=2)
    mine = ResourceArea(100, CollectibleResourceEnum.METAL, x=1, y=2)

    print("\nMINE")
    print(mine)

    print("\nMINE.TELEGRAM_TEXT")
    print(mine.telegram_text)

    print("\nMINE.TO_DICT")
    print(mine.to_dict())

    print(" END LOCAL TEST ".center(79, "="))
