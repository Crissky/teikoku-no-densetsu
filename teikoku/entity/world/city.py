from dataclasses import dataclass, InitVar

from repository.mongo.base import MongoBase
from teikoku.entity.register.player import Player
from teikoku.entity.world.coor import Coordinate


@dataclass
class City(MongoBase):
    name: str
    owner: Player
    x: InitVar[int]
    y: InitVar[int]

    UPDATABLE_ATTR_LIST = ()

    def __post_init__(self, x: int, y: int):
        super().__post_init__()

        if not isinstance(self.name, str):
            e = f"O name precisa ser do tipo str ({type(self.name)})."
            raise TypeError(e)

        if not isinstance(self.owner, Player):
            e = f"owner deve ser do tipo PLayer ({type(self.owner)})"
            raise TypeError(e)

        self.coor = Coordinate(x=x, y=y)

    @property
    def telegram_text(self) -> str:
        text = f"*Cidade*: {self.name}\n"
        text += f"*Governante*: {self.owner.effective_name} "
        text += f"({self.owner.user_id})\n"
        text += f"*Coordenadas*: {self.coor.show}\n"

        return text


if __name__ == "__main__":
    print(" START LOCAL TEST ".center(79, "="))
    p = Player(user_id=123, name="teste")
    city = City(name="Cidade Teste", x=1, y=2, owner=p)

    print("\nCITY:")
    print(city)

    print("\nCITY.TELEGRAM_TEXT:")
    print(city.telegram_text)

    print("\nCITY.TO_DICT:")
    print(city.to_dict())

    print(" END LOCAL TEST ".center(79, "="))
