from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict

from repository.mongo.base import MongoBase
from teikoku.enum.resource import CollectibleResourceEnum


@dataclass
class Bag(MongoBase):
    capacity: int
    items: Dict[CollectibleResourceEnum, int] = field(
        default_factory=defaultdict
    )

    UPDATABLE_ATTR_LIST = ()
