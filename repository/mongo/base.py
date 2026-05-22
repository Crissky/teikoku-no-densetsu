from collections import deque
import logging

from abc import ABC, abstractmethod
from enum import Enum

from dataclasses import dataclass, field, fields
from datetime import datetime
from typing import (
    Any,
    ClassVar,
    List,
    Literal,
    Optional,
    Tuple,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

from bson import ObjectId

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class MongoBase(ABC):
    _id: Union[ObjectId, str] = field(default_factory=ObjectId)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    UPDATABLE_ATTR_LIST: ClassVar[Tuple[str]]

    def __post_init__(self):
        if self._id is None or isinstance(self._id, str):
            self._id = ObjectId(self._id)

        self._check_init_types()

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

    def _check_init_types(self):
        error_list = []
        init_fields = {f.name for f in fields(self) if f.init}
        hints = {
            k: v
            for k, v in get_type_hints(type(self)).items()
            if k in init_fields
        }
        for attr, expected_type in hints.items():
            value = getattr(self, attr)
            error_list.extend(self._validate_type(attr, expected_type, value))

        if error_list:
            raise TypeError("\n".join(error_list))

    def _validate_type(
        self, attr: str, expected_type: type, value: Any
    ) -> List[str]:
        error_list = []
        origin = get_origin(expected_type)
        args = get_args(expected_type)

        if origin is None:
            if not isinstance(value, expected_type):
                error = self._get_msg_error(attr, expected_type, value)
                error_list.append(error)

        elif origin is Union:
            union_error_list = []
            for a in args:
                el = self._validate_type(attr, a, value)
                if not el:
                    union_error_list = []
                    break
                union_error_list.extend(el)

            if union_error_list:
                error_list.append(self._get_msg_error(attr, args, value))

        elif origin is list:
            if not isinstance(value, list):
                error = self._get_msg_error(attr, expected_type, value)
                error_list.append(error)
            else:
                for i, v in enumerate(value):
                    error_list.extend(
                        self._validate_type(f"{attr}.[{i}]", args[0], v)
                    )

        elif origin is deque:
            if not isinstance(value, deque):
                error = self._get_msg_error(attr, expected_type, value)
                error_list.append(error)
            else:
                for i, v in enumerate(value):
                    error_list.extend(
                        self._validate_type(f"{attr}.[{i}]", args[0], v)
                    )

        elif origin is tuple:
            if not isinstance(value, tuple):
                error = self._get_msg_error(attr, expected_type, value)
                error_list.append(error)
            elif len(args) != len(value):
                error = (
                    f"'{attr}' deve ter tamanho {len(args)}, "
                    f"mas recebeu o tamanho {len(value)}."
                )
                error_list.append(error)
            else:
                for i, (a, v) in enumerate(zip(args, value)):
                    error_list.extend(
                        self._validate_type(f"{attr}.[{i}]", a, v)
                    )

        elif origin is dict:
            if not isinstance(value, dict):
                error = self._get_msg_error(attr, expected_type, value)
                error_list.append(error)
            else:
                key_type, value_type = args
                for k, v in value.items():
                    error_list.extend(
                        self._validate_type(f"{attr}['{k}']", value_type, v)
                    )
                    error_list.extend(
                        self._validate_type(f"{attr}['{k}']", key_type, k)
                    )

        elif origin is Optional:
            if value is not None:
                error_list.extend(self._validate_type(attr, args[0], value))

        elif origin is Literal:
            if value not in args:
                error = (
                    f"'{attr}' deve ser um dos valores {args}, "
                    f"mas recebeu o valor {value}."
                )
                error_list.append(error)

        return error_list

    def _get_msg_error(
        self, attr: str, expected_type: type, value: Any
    ) -> str:
        return (
            f"'{attr}' deve ser do tipo {expected_type}, "
            f"mas recebeu o tipo {type(value).__name__}."
        )

    def to_dict(self) -> dict:
        d = {}
        for f in fields(self):
            if not f.init:
                continue

            obj = getattr(self, f.name)
            d[f.name] = self._parse_to_mongo(obj)

        d.update(self.extra_attr)

        return d

    def _parse_to_mongo(self, obj: Any) -> Any:

        if isinstance(obj, list):
            return [self._parse_to_mongo(o) for o in obj]
        elif isinstance(obj, MongoBase):
            return obj.persisted_fields
        elif isinstance(obj, Enum):
            return obj.name
        else:
            return obj

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

    @property
    def persisted_fields(self) -> Union[dict, ObjectId]:
        """Representação da classe quando ela é um atributo de outra classe
        MongoBase.

        Usar self._id se o atributo for instanciado pelo Model, ou seja,
        se o atributo é um documento de uma collection do MongoDB.

        Usar self.to_dict() se o atributo for instanciado pela classe,
        ou seja, se o atributo for um campo Object no MongoDB.
        """

        return self._id

    @property
    def extra_attr(self) -> dict:
        """Atributos extras necessários para instanciar a classe, mas que
        não fazem parte do fields da classe.
        Exemplo: attr que são `InitVar`

        Geralmente precisam ser passados no `**kwargs` do `__post_init__`
        """

        return {}
