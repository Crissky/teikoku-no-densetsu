from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from html import escape
from typing import Deque, Union

from bson import ObjectId

from repository.mongo.base import MongoBase
from teikoku.entity.register.player import Player


@dataclass
class Log(MongoBase):
    max_size: int
    log_list: Deque[str] = field(default_factory=deque, repr=False)

    UPDATABLE_ATTR_LIST = ()

    def __post_init__(self):
        if not isinstance(self.max_size, int):
            e = f"max_size deve ser do tipo int ({type(self.max_size)})."
            raise TypeError(e)
        elif self.max_size <= 0:
            e = f"max_size deve ser maior que zero ({self.max_size})."
            raise ValueError(e)

        if not isinstance(self.log_list, (list, deque)):
            raise TypeError(
                f"log_list deve ser do tipo list ou deque "
                f"({type(self.log_list)})."
            )
        else:
            self.log_list = deque(self.log_list, maxlen=self.max_size)

    def add(self, msg: str, player: Player = None) -> str:
        if isinstance(player, Player):
            msg = f"{player.name}: {msg}"
        msg = f"[{self.timestamp}] - {msg}"
        self.log_list.append(msg)

        return msg

    @property
    def timestamp(self) -> str:

        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def telegram_text(self) -> str:
        return "\n".join((f"  {escape(s)}" for s in self.log_list))

    @property
    def persisted_fields(self) -> Union[dict, ObjectId]:
        return self.to_dict()


if __name__ == "__main__":
    print(" START LOCAL TEST ".center(79, "="))

    log = Log(3, deque())
    log.add("teste 1")
    log.add("teste 2")
    log.add("teste 3")
    log.add("teste 4")
    log.add("teste 5")

    print("\nLOG")
    print(log)

    print("\nLOG.TELEGRAM_TEXT")
    print(log.telegram_text)

    print("\nMINE.TO_DICT")
    print(log.to_dict())

    print(" END LOCAL TEST ".center(79, "="))
