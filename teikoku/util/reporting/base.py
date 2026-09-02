from collections import deque
from dataclasses import dataclass, fields
from enum import Enum
from typing import (
    Any,
    Iterator,
    List,
    Literal,
    Optional,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

from teikoku.enum.reporting import ReportingStatusEnum


@dataclass(kw_only=True, frozen=True)
class ReportingBase:
    message: str
    status: ReportingStatusEnum

    def __post_init__(self):

        self._load_enums()
        self._check_init_types()

    def _load_enums(self):
        type_hints = get_type_hints(type(self))
        for field in fields(self):
            if not field.init:
                continue

            field_type = type_hints.get(field.name)
            if (
                isinstance(field_type, type)
                and issubclass(field_type, Enum)
                and isinstance(getattr(self, field.name), str)
            ):
                object.__setattr__(
                    self,
                    field.name,
                    field_type(getattr(self, field.name)),
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

    def __str__(self):
        return ", ".join(f"{a}={getattr(self, a)}" for a in self.kwargs)

    def __repr__(self):
        text = str(self)
        return f"{self.__class__.__name__}({text})"

    def __getitem__(self, key: str):
        if self.has_attibute(key):
            return getattr(self, key)
        else:
            return None

    def has_attibute(self, attribute: str) -> bool:
        return any(f.name == attribute for f in fields(self) if f.init)

    @property
    def report(self) -> dict:
        return {a: getattr(self, a) for a in self.kwargs}

    @property
    def text(self) -> str:
        return self.message

    @property
    def status_name(self) -> str:
        return self.status.name

    @property
    def status_text(self) -> str:
        return self.status.value

    @property
    def kwargs(self) -> Iterator[str]:
        return (f.name for f in fields(self) if f.init)


if __name__ == "__main__":
    print(" START LOCAL TEST ".center(79, "="))
    r = ReportingBase(
        # city="cidade",
        message="Mensagem de teste.",
        status="success",
    )
    print(r)
    print(repr(r))
    print("REPORT:", r.report)
    print("TEXT:", r.text)
    print("STATUS NAME:", r.status_name)
    print("STATUS TEXT:", r.status_text)
    print(" END LOCAL TEST ".center(79, "="))
