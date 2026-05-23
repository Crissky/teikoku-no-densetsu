from dataclasses import dataclass
from typing import Union

from repository.mongo.base import MongoBase


@dataclass
class StatModifier(MongoBase):
    bonus_hp: Union[int, float]
    bonus_strength: Union[int, float]
    bonus_mind: Union[int, float]
    bonus_defense: Union[int, float]
    bonus_speed: Union[int, float]
    description: str = ""

    UPDATABLE_ATTR_LIST = ()
