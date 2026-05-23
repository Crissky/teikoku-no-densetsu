from dataclasses import InitVar, dataclass, field
from typing import List

from repository.mongo.base import MongoBase
from teikoku.entity.unit.stats_modifier import StatModifier
from teikoku.entity.unit.unit_stats import Stats
from teikoku.enum.unit import UnitNameEnum


@dataclass
class UnitBase(MongoBase):
    name: UnitNameEnum
    level: InitVar[int]
    hp: InitVar[int]
    damaged: InitVar[int]
    power: InitVar[int]
    mind: InitVar[int]
    defense: InitVar[int]
    speed: InitVar[int]
    stat_modifier_list: InitVar[List[StatModifier]] = field(
        default_factory=list
    )
    bag_size: InitVar[int]

    def __post_init__(
        self,
        level: int,
        hp: int,
        damaged: int,
        power: int,
        mind: int,
        defense: int,
        speed: int,
        stat_modifier_list: List[StatModifier],
        bag_size: int,
    ):
        # NAME
        if isinstance(self.name, str):
            self.name = UnitNameEnum[self.name]

        # BAG
        if self.bag_size < 0:
            e = f"bag_size deve ser um inteiro positivo ({self.bag_size})"
            raise ValueError(e)

        # STATS
        self.stats = Stats(
            level=level,
            damaged=damaged,
            base_hp=hp,
            base_strength=power,
            base_mind=mind,
            base_defense=defense,
            base_speed=speed,
            stat_modifier_list=stat_modifier_list,
        )

        super().__post_init__()
