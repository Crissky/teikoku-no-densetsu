from enum import Enum

from teikoku.enum.generic import GenericEnum


class CityStatsEnum(GenericEnum):
    LEVEL = "nível"
    HP = "hp"
    ATTACK = "ataque"
    DEFENSE = "defesa"


class UnitStatsEnum(GenericEnum):
    LEVEL = "nível"
    HP = "hp"
    STRENGTH = "força"
    MIND = "mente"
    DEFENSE = "defesa"
    SPEED = "velocidade"
