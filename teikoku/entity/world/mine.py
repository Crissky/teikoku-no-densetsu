from dataclasses import InitVar, dataclass
from typing import Union

from bson import ObjectId

from repository.mongo.base import MongoBase
from teikoku.enum.resource import LocationResourceEnum, ResourceEnum
from teikoku.entity.world.coor import Coordinate


@dataclass
class Mine(MongoBase):
    resource: int
    resource_name: ResourceEnum
    x: InitVar[int]
    y: InitVar[int]
    location: LocationResourceEnum = LocationResourceEnum.MINE
    level: int = 1

    UPDATABLE_ATTR_LIST = ()

    def __post_init__(self, x: int, y: int):

        # RESOURCE
        if self.resource < 0:
            raise ValueError(
                "O atributo resource precisa ser um valor positivo "
                f"({self.resource})."
            )

        # RESOURCE_NAME
        if isinstance(self.resource_name, str):
            self.resource_name = ResourceEnum[self.resource_name]

        # COORDINATE
        if isinstance(x, int) and isinstance(y, int):
            self.coor = Coordinate(x=x, y=y)
        else:
            raise TypeError(
                "Os atributos x e y precisam ser do tipo int."
                f"x: {type(self.x)} | y: {type(self.y)}"
            )

        super().__post_init__()

        # LOCATION
        if isinstance(self.location, str):
            self.location = LocationResourceEnum(self.location)
        if not isinstance(self.location, LocationResourceEnum):
            raise TypeError(
                "O atributo name precisa ser uma string "
                f"({type(self.location)})."
            )

        # LEVEL
        if not isinstance(self.level, int):
            raise TypeError(
                "O atributo level precisa ser um inteiro "
                f"({type(self.level)})."
            )
        elif self.level < 0:
            raise ValueError(
                "O atributo level precisa ser um valor positivo "
                f"({self.level})."
            )

    @property
    def name(self):
        return (
            f"{self.location.value.title()} de "
            f"{self.resource_name.value.title()}"
        )

    @property
    def telegram_text(self):
        resource_name = self.resource_name.value.title()
        text = f"*Local*: {self.name}\n"
        text += f"*Nível*: {self.level}\n"
        text += f"*{resource_name}*: {self.resource}\n"

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

    mine = Mine(100, "METAL", x=1, y=2)
    mine = Mine(100, ResourceEnum.METAL, x=1, y=2)

    print("\nMINE")
    print(mine)

    print("\nMINE.TELEGRAM_TEXT")
    print(mine.telegram_text)

    print("\nMINE.TO_DICT")
    print(mine.to_dict())

    print(" END LOCAL TEST ".center(79, "="))
