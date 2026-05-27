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
