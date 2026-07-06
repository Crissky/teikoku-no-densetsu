from types import MappingProxyType

# WORLD
DEFAULT_WORLD_CHAT_ID = PUBLIC_WORLD_CHAT_ID = -1


# TERRAIN MAP
DEFAULT_TERRAIN_SIZE = 512
DEFAULT_TERRAIN_SEED = 42
MAX_SEEDS = 1024
IGNORE_SEEDS = [433]
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

# IMAGES =====================================================================
# BASE MAP
MIN_MAP_SIZE = (1024, 1024)

# LEGEND MAP
LEGEND_WORLD_FONT_PATH = "teikoku\assets\fonts\retro_gaming.ttf"
LEGEND_TITLE_SIZE = 16
LEGEND_TEXT_SIZE = 14
LEGEND_BG_COLOR = (30, 30, 30)
LEGEND_TITLE_COLOR = (255, 255, 255)
LEGEND_TEXT_COLOR = (230, 230, 230)
LEGEND_RECT_OUTLINE = (255, 255, 255)
