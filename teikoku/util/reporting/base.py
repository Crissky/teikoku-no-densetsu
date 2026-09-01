from dataclasses import dataclass, fields
from enum import Enum
from typing import Iterator, get_type_hints

from teikoku.enum.reporting import ReportingStatusEnum


@dataclass(kw_only=True, frozen=True)
class ReportingBase:
    message: str
    status: ReportingStatusEnum

    def __post_init__(self):
        type_hints = get_type_hints(type(self))

        # INSTANCIA ENUMS ATRAVÉS DE SEU NOME (STRING)
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

        # self._check_init_types() # TODO copiar e adaptar do `MongoBase`

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
