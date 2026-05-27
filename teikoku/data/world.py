from types import MappingProxyType

DEFAULT_TERRAIN_SIZE = 512
DEFAULT_WORLD_SEED = 42
MIN_MAP_SIZE = (1024, 1024)
PNOISE2_SCALE = 0.005
PNOISE2_CONFIG = MappingProxyType(
    dict(
        octaves=8,
        persistence=0.5,
        lacunarity=3.0,
        repeatx=1024,
        repeaty=1024,
    )
)
TERRAIN_COLORS = MappingProxyType(
    {
        0: (76, 175, 80),  # Grama (Verde padrão)
        1: (13, 71, 161),  # Água Profunda / Oceano (Azul Escuro)
        2: (33, 150, 243),  # Água Rasa (Azul claro)
        3: (203, 189, 147),  # Areia / Praia (Bege)
        4: (27, 94, 32),  # Pântano / Floresta (Verde Escuro)
        5: (139, 195, 74),  # Colinas (Verde Oliva)
        6: (158, 158, 158),  # Montanha (Cinza)
        7: (245, 245, 245),  # Pico Nevado (Branco)
    }
)
GRASSLAND_TERRAIN_NAME = "Grama"
DEEP_SEA_TERRAIN_NAME = "Mar Profundo"
SHALLOW_WATER_TERRAIN_NAME = "Água Rasa"
BEACH_TERRAIN_NAME = "Areia / Praia"
SWANP_FOREST_TERRAIN_NAME = "Pântano / Floresta"
HILLS_TERRAIN_NAME = "Colinas"
MOUNTAIN_TERRAIN_NAME = "Montanha"
SNOW_PEAK_TERRAIN_NAME = "Pico Nevado"
TERRAIN_NAMES = MappingProxyType(
    {
        0: GRASSLAND_TERRAIN_NAME,
        1: DEEP_SEA_TERRAIN_NAME,
        2: SHALLOW_WATER_TERRAIN_NAME,
        3: BEACH_TERRAIN_NAME,
        4: SWANP_FOREST_TERRAIN_NAME,
        5: HILLS_TERRAIN_NAME,
        6: MOUNTAIN_TERRAIN_NAME,
        7: SNOW_PEAK_TERRAIN_NAME,
    }
)
