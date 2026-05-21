from dataclasses import dataclass, field
import logging
from typing import Dict, Optional, Tuple

from repository.mongo.base import MongoBase
from teikoku.entity.world.city import City
from teikoku.entity.world.coor import Coordinate

logger = logging.getLogger(__name__)


@dataclass
class World(MongoBase):
    name: str
    base_size: int = 500
    cities: Dict[Tuple[int, int], City] = field(default_factory=dict)

    UPDATABLE_ATTR_LIST = ()

    def __post_init__(self):

        if self.base_size <= 0:
            raise TypeError(
                "base_size precisa ser um inteiro maior que zero "
                f"({self.base_size})."
            )

        error_cities = []
        for i, city in enumerate(self.cities):
            if not isinstance(city, City):
                error_cities.append((i, type(city)))

        if error_cities:
            e = ", ".join([f" {i} ({t})" for i, t in error_cities])
            raise TypeError(
                "Todos os elementos de cities precisam ser do tipo City. "
                f"Índices com erro:{e}."
            )

        super().__post_init__()

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
    world = World(name="Mundo Teste", cities=[c])

    print("\nWORLD")
    print(world)

    print("\nWORLD.TELEGRAM_TEXT")
    print(world.telegram_text)

    print("\nWORLD.TO_DICT")
    print(world.to_dict())

    print(" END LOCAL TEST ".center(79, "="))
