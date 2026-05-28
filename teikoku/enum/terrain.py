from enum import Enum


class TerrainColorEnum(Enum):
    GRASSLAND = (76, 175, 80)
    DEEP_SEA = (13, 71, 161)
    SHALLOW_WATER = (33, 150, 243)
    BEACH = (203, 189, 147)
    SWAMP_FOREST = (27, 94, 32)
    HILLS = (139, 195, 74)
    MOUNTAIN = (158, 158, 158)
    SNOW_PEAK = (245, 245, 245)


class TerrainNumberEnum(Enum):
    GRASSLAND = 0
    DEEP_SEA = 1
    SHALLOW_WATER = 2
    BEACH = 3
    SWAMP_FOREST = 4
    HILLS = 5
    MOUNTAIN = 6
    SNOW_PEAK = 7


class TerrainTextEnum(Enum):
    GRASSLAND = "Grama"
    DEEP_SEA = "Mar Profundo"
    SHALLOW_WATER = "Água Rasa"
    BEACH = "Areia / Praia"
    SWAMP_FOREST = "Pântano / Floresta"
    HILLS = "Colinas"
    MOUNTAIN = "Montanha"
    SNOW_PEAK = "Pico Nevado"
