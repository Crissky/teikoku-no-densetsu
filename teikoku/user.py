from dataclasses import dataclass
from typing import Union

from repository.mongo.base import MongoBase


@dataclass
class User(MongoBase):
    telegram_id: Union[int, str]
    name: str

    def __post_init__(self):
        super().__post_init__()

        # TELEGRAM ID
        if not self.telegram_id:
            raise ValueError(
                f"O telegram_id '{self.telegram_id}' não é válido."
            )
        elif isinstance(self.telegram_id, int):
            self.telegram_id = str(self.telegram_id)
        if not isinstance(self.telegram_id, str):
            raise TypeError(
                "O telegram_id precisa ser do tipo int ou str "
                f"({type(self.telegram_id)})."
            )

        # NAME
        if self.name is not None:
            self.name = str(self.name)

    def __eq__(self, value):
        result = False
        if isinstance(value, User):
            result = self.telegram_id == value.telegram_id
        elif isinstance(value, str):
            result = self.telegram_id == value
        elif isinstance(value, int):
            result = self.telegram_id == str(value)

        return result

    @property
    def telegram_text(self) -> str:
        text = f"Name: {self.name}\n"
        text += f"Telegram ID: {self.telegram_id}\n"

        return text


if __name__ == "__main__":
    print(" START LOCAL TEST ".center(79, "="))
    user = User(telegram_id=123456789, name="Teste")

    print("\nUSER:")
    print(user)

    print("\nUSER.TELEGRAM_TEXT:")
    print(user.telegram_text)

    print(" END LOCAL TEST ".center(79, "="))
