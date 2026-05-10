from dataclasses import dataclass

from repository.mongo.base import MongoBase


@dataclass
class Player(MongoBase):
    user_id: int  # TELEGRAM ID
    name: str
    username: str = None  # @ do usuário
    silent: bool = False

    def __post_init__(self):
        super().__post_init__()

        # USER ID
        if not self.user_id:
            raise ValueError(f"O user_id '{self.user_id}' não é válido.")
        if not isinstance(self.user_id, int):
            e = f"O user_id precisa ser do tipo int ({type(self.user_id)})."
            raise TypeError(e)

        # NAME
        if self.name is not None:
            self.name = str(self.name)

        # USERNAME
        username = self.username
        if not isinstance(username, (str, type(None))):
            e = f"O username precisa ser do tipo str ({type(username)})."
            raise TypeError(e)
        elif isinstance(username, str) and not username.startswith("@"):
            raise ValueError(
                f"O username '{username}' não é válido "
                "(precisa começar com '@')."
            )

        if not isinstance(self.silent, bool):
            e = f"O silent precisa ser do tipo bool ({type(self.silent)})."
            raise TypeError(e)

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
        text = f"Name: {self.name}\n"
        text += f"Username: {self.username or ''}\n"
        text += f"User ID: {self.user_id}\n"
        text += f"Modo Silencioso: {self.translate(self.silent)}\n"

        return text


if __name__ == "__main__":
    print(" START LOCAL TEST ".center(79, "="))
    player = Player(user_id=123456789, name="Teste")

    print("\nPLAYER:")
    print(player)

    print("\nPLAYER.TELEGRAM_TEXT:")
    print(player.telegram_text)

    print(" END LOCAL TEST ".center(79, "="))
