from dataclasses import dataclass
from typing import Optional

from repository.mongo.base import MongoBase


@dataclass
class Player(MongoBase):
    user_id: int  # TELEGRAM ID
    name: str
    username: Optional[str] = None  # @ do usuário
    silent: bool = False

    UPDATABLE_ATTR_LIST = ("silent",)

    def __post_init__(self):
        # USERNAME
        username = self.username
        if isinstance(username, str) and not username.startswith("@"):
            raise ValueError(
                f"O username '{username}' não é válido "
                "(precisa começar com '@')."
            )

        super().__post_init__()

    def __eq__(self, value):
        result = False
        if isinstance(value, Player):
            result = self.user_id == value.user_id
        elif isinstance(value, str) and value.isnumeric():
            result = self.user_id == int(value)
        elif isinstance(value, int):
            result = self.user_id == value

        return result

    @property
    def telegram_text(self) -> str:
        text = f"*Nome*: {self.name}\n"
        text += f"*Nome de Usuário*: {self.username or ''}\n"
        text += f"*ID de Usuário*: {self.user_id}\n"
        text += f"*Modo Silencioso*: {self.translate(self.silent)}\n"

        return text

    @property
    def effective_name(self) -> str:
        return self.username or self.name


if __name__ == "__main__":
    print(" START LOCAL TEST ".center(79, "="))
    print(f"UPDATABLE_ATTR_LIST: {Player.UPDATABLE_ATTR_LIST}")
    player = Player(user_id=123456789, name="Teste")

    print("\nPLAYER:")
    print(player)

    print("\nPLAYER.TELEGRAM_TEXT:")
    print(player.telegram_text)

    print("\nPLAYER.TO_DICT:")
    print(player.to_dict())

    print(" END LOCAL TEST ".center(79, "="))
