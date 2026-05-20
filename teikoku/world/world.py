from dataclasses import dataclass, field
import logging
from typing import Dict, Optional, Tuple

from repository.mongo.base import MongoBase
from teikoku.world.city import City

logger = logging.getLogger(__name__)


@dataclass
class World(MongoBase):
    name: str
    base_size: int = 500
    cities: Dict[Tuple[int, int], City] = field(default_factory=dict)

    UPDATABLE_ATTR_LIST = tuple()

    def __post_init__(self):
        super().__post_init__()

        if not isinstance(self.name, str):
            e = f"O name precisa ser do tipo str ({type(self.name)})."
            raise TypeError(e)

        if not isinstance(self.base_size, int):
            e = f"base_size precisa ser do tipo int ({type(self.base_size)})."
            raise TypeError(e)

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
    from teikoku.register.player import Player

    print(" START LOCAL TEST ".center(79, "="))
    p = Player(user_id=123, name="teste")
    c = City(name="Cidade Teste", x=1, y=2, owner=p)
    world = World(name="Mundo Teste", cities=[c])

    print("\nWORLD")
    print(world)

    print("\nWORLD.TELEGRAM_TEXT")
    print(world.telegram_text)

    print(" END LOCAL TEST ".center(79, "="))
