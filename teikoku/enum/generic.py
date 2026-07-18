from enum import Enum


class GenericEnum(Enum):

    @property
    def lower_name(self) -> str:
        return self.name.lower()

    @property
    def upper_name(self) -> str:
        return self.name.upper()

    @property
    def lower_value(self) -> str:
        return str(self.value).lower()

    @property
    def upper_value(self) -> str:
        return str(self.value).upper()
