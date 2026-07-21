from dataclasses import dataclass, InitVar
from typing import List, Tuple

from repository.mongo.base import MongoBase
from repository.mongo.enums import field
from teikoku.entity.city.city_stats import CityStats
from teikoku.entity.register.player import Player
from teikoku.entity.unit.stats_modifier import StatModifier
from teikoku.entity.world.coor import Coordinate


@dataclass
class City(MongoBase):
    name: str
    chat_id: int
    owner: Player
    x: InitVar[int]
    y: InitVar[int]
    level: InitVar[int]
    damaged: InitVar[int]
    hp: InitVar[int]
    attack: InitVar[int]
    defense: InitVar[int]
    size: int
    stat_modifier_list: InitVar[List[StatModifier]] = field(default=None)

    UPDATABLE_ATTR_LIST = ()

    def __post_init__(
        self,
        x: int,
        y: int,
        level: int,
        damaged: int,
        hp: int,
        attack: int,
        defense: int,
        stat_modifier_list: List[StatModifier],
    ):
        self.hp = 1000
        self.attack = 10
        self.defense = 10

        # COORDINATE
        self.coor = Coordinate(x=x, y=y)

        # STATS
        self.stats = CityStats(
            level=level,
            damaged=damaged,
            base_hp=hp,
            base_attack=attack,
            base_defense=defense,
            stat_modifier_list=stat_modifier_list,
        )

        if self.size % 2 == 0:
            raise ValueError(f"size deve ser ímpar ({self.size}).")

        super().__post_init__()

    def __eq__(self, value):
        result = False
        if isinstance(value, City):
            result = (
                self.user_id == value.user_id and self.chat_id == value.chat_id
            )
        elif isinstance(value, str) and value.isnumeric():
            result = self.user_id == int(value)
        elif isinstance(value, int):
            result = self.user_id == value

        return result

    @property
    def telegram_text(self) -> str:
        text = f"*Cidade*: {self.name}\n"
        text += f"*Governante*: {self.user_name} "
        text += f"({self.user_id})\n"
        text += f"*Coordenadas*: {self.coor.show}\n"

        return text

    @property
    def user_id(self) -> int:
        return self.owner.user_id

    @property
    def user_name(self) -> str:
        self.owner.effective_name

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

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["owner"] = self.user_id

        return d


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
