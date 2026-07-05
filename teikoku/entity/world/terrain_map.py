import logging

from dataclasses import dataclass, field
from typing import Iterable, List, Optional, Tuple

import noise

from teikoku.data.world import (
    DEFAULT_TERRAIN_SIZE,
    DEFAULT_TERRAIN_SEED,
    IGNORE_SEEDS,
    PNOISE2_CONFIG,
    PNOISE2_SCALE,
)
from teikoku.entity.world.coor import Coordinate
from teikoku.entity.world.terrain_info import TerrainInfo
from teikoku.enum.terrain import TerrainNumberEnum

logger = logging.getLogger(__name__)


@dataclass
class TerrainMap:
    size: int = DEFAULT_TERRAIN_SIZE
    central_coor: Coordinate = field(default_factory=Coordinate)
    scale: float = PNOISE2_SCALE
    seed: int = DEFAULT_TERRAIN_SEED

    def __post_init__(self):
        self.map = []

    def __getitem__(self, key):
        if isinstance(key, tuple):
            x, y = key
            return self.map[y][x]
        else:
            return self.map[key]

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            x, y = key
            self.map[y][x] = value
        else:
            self.map[key] = value

    def __iter__(self):
        yield from self.map

    def __len__(self):
        length = 0
        for row in self:
            length += len(row)

        return length

    def generate_terrain_map(
        self,
        central_coor: Optional[Coordinate] = None,
        size: Optional[int] = None,
        scale: Optional[float] = None,
        seed: Optional[int] = None,
    ) -> List[List[int]]:
        if central_coor is None:
            central_coor = self.central_coor
        if size is None:
            size = self.size
        if scale is None:
            scale = self.scale
        if seed is None:
            seed = self.seed

        seed = self.normalize_seed(seed)
        half_size1 = size // 2
        half_size2 = half_size1 if size % 2 == 0 else half_size1 + 1
        x1 = central_coor.x - half_size1
        x2 = central_coor.x + half_size2
        y1 = central_coor.y - half_size1
        y2 = central_coor.y + half_size2
        self.map = []
        logger.info(f"GEN_TERRAIN - x1: {x1}, x2: {x2}, y1: {y1}, y2: {y2}")
        for y in range(y1, y2):
            self.map.append([])
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
                self.map[-1].append(terrain)

        return self.map

    def normalize_seed(self, seed):
        seed = seed % 512
        if seed in IGNORE_SEEDS:
            seed = self.normalize_seed(seed)

        return seed

    @property
    def flatten(self) -> Iterable:
        for row in self.map:
            yield from row

    @property
    def size_x(self):
        return len(self.map[0]) if self.map else 0

    @property
    def size_y(self):
        return len(self.map)

    def value_to_info(self, terrain_value: int) -> TerrainInfo:
        return TerrainInfo(terrain_value)

    def value_to_color(self, terrain_value: int) -> Tuple[int, int, int]:
        terrain_info = self.value_to_info(terrain_value)
        terrain_color = terrain_info.color

        return terrain_color

    def value_to_text(self, terrain_value: int) -> str:
        terrain_info = self.value_to_info(terrain_value)
        terrain_text = terrain_info.text

        return terrain_text

    def get_value(
        self, x: int = None, y: int = None, coordinate: Coordinate = None
    ) -> int:
        if isinstance(coordinate, Coordinate):
            x = coordinate.x
            y = coordinate.y
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError("x e y precisam ser inteiros")

        terrain_value = self[x, y]
        return terrain_value

    def get_color(
        self, x: int = None, y: int = None, coordinate: Coordinate = None
    ) -> Tuple[int, int, int]:
        terrain_value = self.get_value(x, y, coordinate)
        terrain_color = self.value_to_color(terrain_value)

        return terrain_color

    def get_text(
        self, x: int = None, y: int = None, coordinate: Coordinate = None
    ) -> str:
        terrain_value = self.get_value(x, y, coordinate)
        terrain_text = self.value_to_text(terrain_value)

        return terrain_text


if __name__ == "__main__":

    print(" START LOCAL TEST ".center(79, "="))
    map = TerrainMap()

    print("\nTERRAINMAP")
    print(map)

    print("\nTERRAINMAP.GENERATE_TERRAIN_MAP")
    print(map.generate_terrain_map(size=10))

    print("\nTERRAINMAP.GET_COLOR")
    print(map.get_color(0, 0))

    print("\nTERRAINMAP.GET_TEXT")
    print(map.get_text(0, 0))

    print("\nTERRAINMAP.LEN")
    print(len(map))

    print(" END LOCAL TEST ".center(79, "="))
