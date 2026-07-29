from types import MappingProxyType

# WORLD
DEFAULT_WORLD_CHAT_ID = PUBLIC_WORLD_CHAT_ID = -1


# TERRAIN MAP
DEFAULT_TERRAIN_SIZE = 512
DEFAULT_TERRAIN_SEED = 42
MAX_SEEDS = 1024
IGNORE_SEEDS = [
    225,
    227,
    232,
    235,
    240,
    241,
    242,
    244,
    250,
    252,
    255,
    274,
    302,
    310,
    311,
    312,
    325,
    335,
    336,
    337,
    339,
    340,
    341,
    347,
    349,
    353,
    355,
    356,
    358,
    359,
    360,
    361,
    363,
    367,
    368,
    369,
    370,
    378,
    383,
    384,
    385,
    386,
    387,
    388,
    389,
    390,
    392,
    393,
    394,
    395,
    396,
    397,
    400,
    401,
    402,
    404,
    405,
    406,
    408,
    409,
    410,
    411,
    412,
    413,
    414,
    415,
    416,
    417,
    418,
    419,
    420,
    421,
    422,
    423,
    424,
    425,
    426,
    432,
    433,
]
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
