from collections import deque
from dataclasses import dataclass, field
from html import escape
from itertools import islice
from typing import Deque, List, Union

from bson import ObjectId

from general.functions.date_time import get_brazil_time_now
from repository.mongo.base import MongoBase
from teikoku.entity.register.player import Player


@dataclass
class Log(MongoBase):
    max_show: int = 10
    list_size: int = 100
    log_list: Union[Deque[str], List[str]] = field(
        default_factory=deque, repr=False
    )

    UPDATABLE_ATTR_LIST = ()

    def __post_init__(self):
        if self.max_show <= 0:
            e = f"max_show deve ser maior que zero ({self.max_show})."
            raise ValueError(e)
        if self.list_size <= 0:
            e = f"list_size deve ser maior que zero ({self.list_size})."
            raise ValueError(e)
        if self.max_show > self.list_size:
            raise ValueError(
                f"max_show ({self.max_show}) deve ser menor ou igual a "
                f"list_size ({self.list_size})."
            )

        self.log_list = deque(self.log_list, maxlen=self.list_size)
        super().__post_init__()

    def __len__(self) -> int:
        return len(self.log_list)

    def add(self, msg: str, player: Player = None) -> str:
        if isinstance(player, Player):
            msg = f"{player.name}: {msg}"
        msg = f"[{self.timestamp}] - {msg}"
        self.log_list.append(msg)

        return msg

    @property
    def timestamp(self) -> str:
        now = get_brazil_time_now()

        return now.strftime("%Y-%m-%d %H:%M:%S")

    @property
    def telegram_text(self) -> str:
        stop = len(self)
        start = stop - self.max_show

        return "\n".join(
            (f"  {escape(s)}" for s in islice(self.log_list, start, stop))
        )

    @property
    def persisted_fields(self) -> Union[dict, ObjectId]:
        return self.to_dict()


if __name__ == "__main__":
    print(" START LOCAL TEST ".center(79, "="))

    log = Log(max_show=3, list_size=10, log_list=deque())
    for i in range(1, 21):
        log.add(f"teste {i}")

    print("\nLOG")
    print(log)

    print("\nLOG.TELEGRAM_TEXT")
    print(log.telegram_text)

    print("\nMINE.TO_DICT")
    print(log.to_dict())

    print(" END LOCAL TEST ".center(79, "="))
