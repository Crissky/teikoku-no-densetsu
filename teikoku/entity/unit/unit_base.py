from dataclasses import InitVar, dataclass, field
from typing import Dict, List

from repository.mongo.base import MongoBase
from teikoku.data.unit import DEFAULT_BAG_CAPACITY
from teikoku.entity.unit.stats_modifier import StatModifier
from teikoku.entity.utils.bag import Bag
from teikoku.entity.unit.unit_stats import Stats
from teikoku.util.coor import Coordinate
from teikoku.enum.resource import CollectibleResourceEnum
from teikoku.enum.unit import UnitCategoryEnum


@dataclass
class UnitBase(MongoBase):
    name: str
    owner_id: int
    x: InitVar[int]
    y: InitVar[int]
    level: InitVar[int]
    hp: InitVar[int]
    damaged: InitVar[int]
    power: InitVar[int]
    mind: InitVar[int]
    defense: InitVar[int]
    speed: InitVar[int]
    category: UnitCategoryEnum = None
    stat_modifier_list: InitVar[List[StatModifier]] = field(default=None)
    bag_capacity: InitVar[int] = DEFAULT_BAG_CAPACITY
    bag_items: InitVar[Dict[CollectibleResourceEnum, int]] = field(
        default=None
    )

    UPDATABLE_ATTR_LIST = ()

    def __post_init__(
        self,
        x: int,
        y: int,
        level: int,
        hp: int,
        damaged: int,
        power: int,
        mind: int,
        defense: int,
        speed: int,
        stat_modifier_list: List[StatModifier],
        bag_capacity: int,
        bag_items: Dict[CollectibleResourceEnum, int],
    ):
        # COORDINATE
        self.coor = Coordinate(x=x, y=y)

        # NAME
        if isinstance(self.name, str):
            self.name = UnitCategoryEnum[self.name]

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

        # BAG
        if self.bag_capacity < 0:
            e = f"bag_size deve ser um inteiro positivo ({self.bag_capacity})"
            raise ValueError(e)
        self.bag = Bag(capacity=bag_capacity, items=bag_items)

        super().__post_init__()
