from dataclasses import dataclass
from functools import cached_property
from typing import Tuple

from teikoku.enum.terrain import (
    TerrainColorEnum,
    TerrainNumberEnum,
    TerrainTextEnum,
)


@dataclass
class TerrainInfo:
    terrain_value: int

    def __post_init__(self):
        if not isinstance(self.terrain_value, int):
            raise TypeError("terrain_value deve ser um inteiro")

    @cached_property
    def enum_name(self) -> str:
        enum_name = TerrainNumberEnum(self.terrain_value).name
        return enum_name

    @cached_property
    def color(self) -> Tuple[int, int, int]:
        color = TerrainColorEnum[self.enum_name].value
        return color

    @cached_property
    def text(self) -> str:
        text = TerrainTextEnum[self.enum_name].value
        return text


if __name__ == "__main__":
    print(" START LOCAL TEST ".center(79, "="))

    t = TerrainInfo(terrain_value=0)
    print(f"\nTERRAININFO.ENUM_NAME: {t.enum_name}")
    print(f"\nTERRAININFO.COLOR: {t.color}")
    print(f"\nTERRAININFO.TEXT: {t.text}")

    print(" END LOCAL TEST ".center(79, "="))
