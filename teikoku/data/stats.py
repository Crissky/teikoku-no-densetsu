from types import MappingProxyType

LEVEL_GROWUP = MappingProxyType(
    dict(
        hp=100,
        strength=10,
        mind=10,
        defense=10,
        speed=10,
    )
)

CITY_LEVEL_GROWUP = MappingProxyType(
    dict(
        hp=1000,
        attack=100,
        defense=100,
    )
)
