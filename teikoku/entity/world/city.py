from dataclasses import dataclass, InitVar
from typing import Tuple

from repository.mongo.base import MongoBase
from teikoku.entity.register.player import Player
from teikoku.entity.world.coor import Coordinate


@dataclass
class City(MongoBase):
    name: str
    owner: Player
    level: int
    size: int
    x: InitVar[int]
    y: InitVar[int]

    UPDATABLE_ATTR_LIST = ()

    def __post_init__(self, x: int, y: int):
        if self.size % 2 == 0:
            raise ValueError(f"size deve ser ímpar ({self.size}).")

        self.coor = Coordinate(x=x, y=y)
        super().__post_init__()

    @property
    def telegram_text(self) -> str:
        text = f"*Cidade*: {self.name}\n"
        text += f"*Governante*: {self.owner.effective_name} "
        text += f"({self.owner.user_id})\n"
        text += f"*Coordenadas*: {self.coor.show}\n"

        return text

    @property
    def extra_attr(self) -> dict:
        return {
            "x": self.coor.x,
            "y": self.coor.y,
        }

    @property
    def x1(self) -> int:
        return self.coor.x - (self.size // 2)

    @property
    def y1(self) -> int:
        return self.coor.y - (self.size // 2)

    @property
    def x2(self) -> int:
        return self.coor.x + (self.size // 2)

    @property
    def y2(self) -> int:
        return self.coor.y + (self.size // 2)

    @property
    def box(self) -> Tuple[int, int, int, int]:
        """Tuple(x1, y1, x2, y2)"""
        return (self.x1, self.y1, self.x2, self.y2)


if __name__ == "__main__":
    print(" START LOCAL TEST ".center(79, "="))
    p = Player(user_id=123, name="teste")
    city = City(name="Cidade Teste", size=3, x=1, y=2, owner=p)

    print("\nCITY:")
    print(city)

    print("\nCITY.TELEGRAM_TEXT:")
    print(city.telegram_text)

    print("\nCITY.TO_DICT:")
    print(city.to_dict())

    print("\nCITY.BOX:")
    print(city.box)

    print(" END LOCAL TEST ".center(79, "="))
