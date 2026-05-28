import logging

from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple

import noise

from repository.mongo.base import MongoBase
from teikoku.data.world import (
    DEFAULT_WORLD_SEED,
    DEFAULT_TERRAIN_SIZE,
    PNOISE2_CONFIG,
    PNOISE2_SCALE,
)
from teikoku.entity.unit.unit_base import UnitBase
from teikoku.entity.world.city import City
from teikoku.entity.world.coor import Coordinate
from teikoku.enum.terrain import TerrainColorEnum, TerrainNumberEnum

logger = logging.getLogger(__name__)


@dataclass
class World(MongoBase):
    name: str
    cities: Dict[Tuple[int, int], City] = field(default_factory=dict)
    units: Dict[Tuple[int, int], UnitBase] = field(default_factory=dict)

    UPDATABLE_ATTR_LIST = ()

    def generate_partial_terrain_map(
        self,
        coor: Coordinate = Coordinate(0, 0),
        size: int = DEFAULT_TERRAIN_SIZE,
        scale: float = PNOISE2_SCALE,
        seed: int = DEFAULT_WORLD_SEED,
    ):
        half_size1 = size // 2
        half_size2 = half_size1 if size % 2 == 0 else half_size1 + 1
        x1 = coor.x - half_size1
        x2 = coor.x + half_size2
        y1 = coor.y - half_size1
        y2 = coor.y + half_size2
        terrain_map = []
        print(f"x1: {x1}, x2: {x2}, y1: {y1}, y2: {y2}")
        for y in range(y1, y2):
            terrain_map.append([])
            for x in range(x1, x2):
                value = noise.pnoise2(
                    x * scale + seed,
                    y * scale + seed,
                    base=seed,
                    **PNOISE2_CONFIG,
                )

                # --- ÁREA DA ÁGUA (Abaixo de -0.12) ---
                terrain = TerrainNumberEnum.GRASSLAND.value
                if value < -0.32:
                    terrain = TerrainNumberEnum.DEEP_SEA.value
                elif value < -0.2:
                    terrain = TerrainNumberEnum.SHALLOW_WATER.value
                elif value < -0.12:
                    terrain = TerrainNumberEnum.BEACH.value

                # --- ÁREA DA TERRA PLANA E BIOMAS (Entre -0.12 e 0.25) ---
                elif value < -0.05:
                    terrain = TerrainNumberEnum.SWAMP_FOREST.value
                elif value < 0.18:
                    terrain = TerrainNumberEnum.GRASSLAND.value
                elif value < 0.25:
                    terrain = TerrainNumberEnum.HILLS.value

                # --- ÁREA DAS ALTITUDES (Acima de 0.25) ---
                elif value < 0.36:
                    terrain = TerrainNumberEnum.MOUNTAIN.value
                else:
                    terrain = TerrainNumberEnum.SNOW_PEAK.value
                terrain_map[-1].append(terrain)

        return terrain_map

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
    def total_cities(self) -> int:
        return len(self.cities)

    @property
    def telegram_text(self):
        text = f"*Mundo*: {self.name}\n"
        text += f"*Total de Cidades*: {self.total_cities}\n"

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

    print("\nWORLD.GENERATE_PARTIAL_TERRAIN_MAP")
    print(world.generate_partial_terrain_map(size=10))

    print(" END LOCAL TEST ".center(79, "="))
