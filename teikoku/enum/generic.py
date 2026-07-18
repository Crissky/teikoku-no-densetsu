from enum import Enum


class GenericEnum(Enum):

    @property
    def lower(self) -> str:
        return self.name.lower()
