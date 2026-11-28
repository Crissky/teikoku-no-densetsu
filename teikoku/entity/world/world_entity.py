from dataclasses import InitVar, field
from typing import List

from repository.mongo.base import MongoBase
from teikoku.entity.unit.stats_modifier import StatModifier


class WorldEntity(MongoBase):
    name: str
    owner_id: int
    x: InitVar[int]
    y: InitVar[int]
    level: InitVar[int]
    damaged: InitVar[int]
    base_strength: InitVar[int]
    base_dexterity: InitVar[int]
    base_vitality: InitVar[int]
    base_intelligence: InitVar[int]
    base_spirit: InitVar[int]
    base_faith: InitVar[int]
    base_hp: InitVar[int]
    base_physical_attack: InitVar[int]
    base_physical_defense: InitVar[int]
    base_magical_attack: InitVar[int]
    base_magical_defense: InitVar[int]
    base_speed: InitVar[int]
    base_luck: InitVar[int]
    stat_modifier_list: InitVar[List[StatModifier]] = field(default=None)
