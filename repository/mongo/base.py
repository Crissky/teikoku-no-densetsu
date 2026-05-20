import logging

from abc import ABC, abstractmethod
from enum import Enum

from dataclasses import asdict, dataclass, field, fields
from datetime import datetime
from typing import Any, ClassVar, Tuple, Union

from bson import ObjectId

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class MongoBase(ABC):
    _id: Union[ObjectId, str] = field(default_factory=ObjectId)
    created_at: datetime = None
    updated_at: datetime = None
    UPDATABLE_ATTR_LIST: ClassVar[Tuple[str]]

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

    def __init_subclass__(cls):
        super().__init_subclass__()

        if "UPDATABLE_ATTR_LIST" not in cls.__dict__:
            raise TypeError(
                f"{cls.__name__} precisa definir UPDATABLE_ATTR_LIST"
            )

        if not isinstance(cls.UPDATABLE_ATTR_LIST, tuple):
            raise TypeError("UPDATABLE_ATTR_LIST deve ser uma tuple[str, ...]")

        if not all(isinstance(x, str) for x in cls.UPDATABLE_ATTR_LIST):
            raise TypeError(
                "Todos os itens de UPDATABLE_ATTR_LIST devem ser string"
            )

    def to_dict(self) -> dict:
        data = asdict(self)
        d = {}
        for f in fields(self):
            if not f.init:
                continue

            obj = getattr(self, f.name)
            if isinstance(obj, MongoBase):
                d[f.name] = obj._id
            elif isinstance(obj, Enum):
                d[f.name] = obj.name
            else:
                data[f.name]

        return d

    def translate(self, value: Any) -> Union[str, Any]:
        if value is True:
            value = "Sim"
        elif value is False:
            value = "Não"

        return value

    def has_updatable_attr(self, attr: str) -> bool:
        return attr in self.UPDATABLE_ATTR_LIST

    @property
    @abstractmethod
    def telegram_text(self) -> str: ...
