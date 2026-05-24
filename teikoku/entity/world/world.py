from dataclasses import dataclass, field
import logging
import random
from typing import Dict, List, Optional, Tuple

from repository.mongo.base import MongoBase
from teikoku.data.world import TERRAIN_PROBABILITIES
from teikoku.entity.unit.unit_base import UnitBase
from teikoku.entity.world.city import City
from teikoku.entity.world.coor import Coordinate

logger = logging.getLogger(__name__)


@dataclass
class World(MongoBase):
    name: str
    base_size: int = 500
    cities: Dict[Tuple[int, int], City] = field(default_factory=dict)
    units: Dict[Tuple[int, int], UnitBase] = field(default_factory=dict)
    terrain_map: List[List[int]] = field(default_factory=list)

    UPDATABLE_ATTR_LIST = ()

    def __post_init__(self):

        if self.base_size <= 0:
            raise TypeError(
                "base_size precisa ser um inteiro maior que zero "
                f"({self.base_size})."
            )

        if not self.terrain_map:
            self.terrain_map = self.create_terrain_map()

        super().__post_init__()

    def generate_terrain_map(self, seed: int = 42):
        choices = []
        local_rng = random.Random(seed)
        for terrain_id, weight in TERRAIN_PROBABILITIES.items():
            choices.extend([terrain_id] * weight)

        return [
            [local_rng.choice(choices) for _ in range(self.base_size)]
            for _ in range(self.base_size)
        ]

    def add_city(self, city: City):
        if not isinstance(city, City):
            raise TypeError(f"city precisa ser do tipo City ({type(city)}).")

        x = city.coor.x
        y = city.coor.y
        coor = (x, y)
        existing_city = self.cities.get(coor)

        if existing_city is None:
            self.cities[coor] = city
            logger.info(f"Cidade {city.name} adicionada ao Mundo {self.name}.")
        else:
            logger.warning(
                f"Cidade {city.name} NÃO foi adicionada ao Mundo {self.name}, "
                f"por já existir a cidade {existing_city.name} na posição "
                f"{city.coor.show}."
            )

    def get_city(
        self,
        coordinate: Optional[Coordinate],
        x: Optional[int],
        y: Optional[int],
    ) -> Optional[City]:
        if isinstance(coordinate, Coordinate):
            x = coordinate.x
            y = coordinate.y

        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError(
                "Os parâmetros x e y precisam ser do tipo int."
                f"x: {type(x)} | y: {type(y)}"
            )

        coor = (x, y)

        return self.cities.get(coor, None)

    @property
    def size(self) -> int:
        total_cities = max(self.total_cities, 1)
        return self.base_size * total_cities

    @property
    def total_cities(self) -> int:
        return len(self.cities)

    @property
    def telegram_text(self):
        text = f"*Mundo*: {self.name}\n"
        text += f"*Total de Cidades*: {self.total_cities}\n"
        text += f"*Tamanho*: {self.size} unidades\n"

        return text


if __name__ == "__main__":
    from teikoku.entity.register.player import Player

    print(" START LOCAL TEST ".center(79, "="))
    p = Player(user_id=123, name="teste")
    c = City(name="Cidade Teste", x=1, y=2, owner=p)
    cities = {(c.coor.x, c.coor.y): c}
    world = World(name="Mundo Teste", cities=cities)

    print("\nWORLD")
    print(world)

    print("\nWORLD.TELEGRAM_TEXT")
    print(world.telegram_text)

    print("\nWORLD.TO_DICT")
    print(world.to_dict())

    print(" END LOCAL TEST ".center(79, "="))
