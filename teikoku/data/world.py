from types import MappingProxyType

DEFAULT_TERRAIN_SIZE = 512
DEFAULT_WORLD_SEED = 42
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
TERRAIN_NAMES = MappingProxyType(
    {
        0: "Grama",
        1: "Mar Profundo",
        2: "Água Rasa",
        3: "Areia / Praia",
        4: "Pântano / Floresta",
        5: "Colinas",
        6: "Montanha",
        7: "Pico Nevado",
    }
)
