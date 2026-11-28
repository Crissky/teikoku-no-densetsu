from dataclasses import dataclass
from typing import Any, Tuple, Type, Union

from repository.mongo.base import MongoBase
from teikoku.enum.stats import BaseStatsEnum
from teikoku.util.enum import try_enum


@dataclass
class BaseStats(MongoBase):

    def __getitem__(self, name: Union[BaseStatsEnum, str]) -> Any:
        name = self.get_enum_stats(name)
        attr_name = self.prefix + name.value
        return getattr(self, attr_name)

    def __setitem__(self, name: BaseStatsEnum, value):
        name = self.get_enum_stats(name)
        attr_name = self.prefix + name.value
        return setattr(self, attr_name, value)

    def get_enum_stats(self, name: str) -> BaseStatsEnum:
        """Transforma a str em um dos BaseStatsEnum de self.enum_stats."""

        if isinstance(name, str):
            for enum_class in self.enum_stats:
                temp_name = try_enum(enum_class, name)
                if temp_name is not None:
                    name = temp_name
                    break
        if not isinstance(name, self.enum_stats):
            TypeError(
                f"name deve ser do tipo {self.enum_stats}. Tipo: {type(name)}."
            )

        return name

    @property
    def enum_stats(self) -> Tuple[Type[BaseStatsEnum]]:
        """Retorna as classes de enums que podem ser usadas para o getitem e
        setitem dessa objeto.
        """

        return (BaseStatsEnum,)

    @property
    def prefix(self) -> str:
        """Prefixo usado para o getitem e setitem dos stats.

        Exemplo: prefix = 'base_' e name do getitem = 'attack', o atributo que
        será acessado é o 'base_attack'.
        """

        return ""
