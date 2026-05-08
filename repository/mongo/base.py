import logging

from dataclasses import asdict, dataclass, field, fields
from datetime import datetime
from typing import Union

from bson import ObjectId

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class MongoBase:
    _id: Union[ObjectId, str] = field(default_factory=ObjectId)
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        if self._id is None or isinstance(self._id, str):
            self._id = ObjectId(self._id)
        if not isinstance(self._id, ObjectId):
            raise TypeError(
                f"O _id passado é do tipo inválido. ({type(self._id)})"
            )

        if not isinstance(self.created_at, (datetime, type(None))):
            raise TypeError(
                "O created_at passado é do tipo inválido. "
                f"({type(self.created_at)})"
            )

        if not isinstance(self.updated_at, (datetime, type(None))):
            raise TypeError(
                "O updated_at passado é do tipo inválido. "
                f"({type(self.updated_at)})"
            )

    def to_dict(self):
        data = asdict(self)
        self_fields = fields(self)

        return {f.name: data[f.name] for f in self_fields if f.init}
