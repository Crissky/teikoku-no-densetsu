from teikoku.enum.generic import GenericEnum


class BaseStatsEnum(GenericEnum): ...


class BasicStatsEnum(GenericEnum):
    LEVEL = "level"
    STRENGTH = "strength"
    DEXTERITY = "dexterity"
    VITALITY = "vitality"
    INTELLIGENCE = "intelligence"
    SPIRIT = "spirit"
    FAITH = "faith"


class CombatStatsEnum(GenericEnum):
    HP = "hp"
    PHYSICAL_ATTACK = "physical_attack"
    PHYSICAL_DEFENSE = "physical_defense"
    MAGICAL_ATTACK = "magical_attack"
    MAGICAL_DEFENSE = "magical_defense"
    SPEED = "speed"
    LUCK = "luck"
