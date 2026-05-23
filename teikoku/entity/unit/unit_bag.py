from dataclasses import dataclass
from typing import Dict

from repository.mongo.base import MongoBase
from teikoku.enum.resource import CollectibleResourceEnum


@dataclass
class UnitBag(MongoBase):
    capacity: int
    items: Dict[CollectibleResourceEnum, int]

    UPDATABLE_ATTR_LIST = ()
