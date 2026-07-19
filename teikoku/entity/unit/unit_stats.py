from dataclasses import dataclass, field, fields
from typing import List

from repository.mongo.base import MongoBase
from teikoku.data.stats import LEVEL_GROWUP
from teikoku.entity.unit.stats_modifier import StatModifier
from teikoku.enum.stats import UnitStatsEnum


@dataclass
class Stats(MongoBase):
    level: int
    damaged: int
    base_hp: int
    base_strength: int
    base_mind: int
    base_defense: int
    base_speed: int
    stat_modifier_list: List[StatModifier] = field(default_factory=list)

    UPDATABLE_ATTR_LIST = ()

    def __post_init__(self):
        # LEVEL
        if self.level <= 0:
            raise ValueError(f"level deve ser maior que zero ({self.level})")

        # DAMAGED
        if self.damaged < 0:
            e = f"damaged deve ser um inteiro positivo ({self.damaged})"
            raise ValueError(e)

        # BASE STATS
        attr_fields = fields(self)
        for attr in attr_fields:
            if not attr.name.startswith("base_"):
                continue
            attr_value = getattr(self, attr.name)
            if attr_value <= 0:
                e = f"{attr.name} deve ser maior que zero ({attr_value})"
                raise ValueError(e)

        super().__post_init__()

    def add_damage(self, damage: int):
        if damage < 0:
            raise ValueError(f"damage deve ser um inteiro positivo ({damage})")

        self.damaged += damage
        self.damaged = min(self.damaged, self.base_hp)

    def heal_damage(self, heal: int):
        if heal < 0:
            raise ValueError(f"heal deve ser um inteiro positivo ({heal})")

        self.damaged -= heal
        self.damaged = max(self.damaged, 0)

    def _get_modified_stat(
        self,
        attr_enum: UnitStatsEnum,
    ) -> int:
        """Retorna o valor modificado de um atributo base."""

        attr = attr_enum.lower_name
        base_attr_value = getattr(self, f"base_{attr}")
        adder_value = 0
        multiplier_value = 1.0
        level_growup = self.level * LEVEL_GROWUP[attr]
        for stat_modifier in self.stat_modifier_list:
            modifier_value = getattr(stat_modifier, f"bonus_{attr}")
            if isinstance(modifier_value, int):
                adder_value += modifier_value
            elif isinstance(modifier_value, float):
                multiplier_value += modifier_value

        modified_stat = int(
            ((base_attr_value + adder_value) * multiplier_value) + level_growup
        )

        return max(modified_stat, 1)

    # REAL STATS
    @property
    def hp(self) -> int:
        return self._get_modified_stat(UnitStatsEnum.HP)

    @property
    def strength(self) -> int:
        return self._get_modified_stat(UnitStatsEnum.STRENGTH)

    @property
    def mind(self) -> int:
        return self._get_modified_stat(UnitStatsEnum.MIND)

    @property
    def defense(self) -> int:
        return self._get_modified_stat(UnitStatsEnum.DEFENSE)

    @property
    def speed(self) -> int:
        return self._get_modified_stat(UnitStatsEnum.SPEED)

    @property
    def current_hp(self) -> int:
        current = self.hp - self.damaged

        return max(current, 0)

    @property
    def hp_rate(self) -> float:
        return self.current_hp / self.hp

    @property
    def is_alive(self) -> bool:
        return bool(self.current_hp > 0)

    @property
    def is_dead(self) -> bool:
        return not self.is_alive

    @property
    def is_full_hp(self) -> bool:
        return self.current_hp == self.hp

    @property
    def level_emoji(self) -> str:
        return "*⭐LV*"

    @property
    def hp_emoji(self) -> str:
        emoji = ""
        if self.is_full_hp:
            emoji = "💖"
        elif self.is_dead:
            emoji = "💀"
        elif not self.is_full_hp:
            emoji = "❤️‍🩹"

        return f"*{emoji}HP*"

    @property
    def strength_emoji(self) -> str:
        return "*🏋️FOR*"

    @property
    def mind_emoji(self) -> str:
        return "*🧠MEN*"

    @property
    def defense_emoji(self) -> str:
        return "*🛡️DEF*"

    @property
    def speed_emoji(self) -> str:
        return "*🏃VEL*"

    @property
    def show_hp(self) -> str:
        return f"{self.current_hp}/{self.hp}"

    @property
    def telegram_text(self) -> str:
        return (
            f"{self.level_emoji}: {self.level}\n"
            f"{self.hp_emoji}: {self.show_hp}({self.base_hp})\n"
            f"{self.strength_emoji}: {self.strength}({self.base_strength})\n"
            f"{self.mind_emoji}: {self.mind}({self.base_mind})\n"
            f"{self.defense_emoji}: {self.defense}({self.base_defense})\n"
            f"{self.speed_emoji}: {self.speed}({self.base_speed})\n"
        )


if __name__ == "__main__":
    print(" START LOCAL TEST ".center(79, "="))
    stats = Stats(
        level=1,
        damaged=10,
        base_hp=100,
        base_strength=10,
        base_mind=10,
        base_defense=10,
        base_speed=10,
    )

    print("\nSTATS")
    print(stats)

    print("\nSTATS.TELEGRAM_TEXT")
    print(stats.telegram_text)

    print("\nSTATS.TO_DICT")
    print(stats.to_dict())

    print(" END LOCAL TEST ".center(79, "="))
