from dataclasses import dataclass

from repository.mongo.base import MongoBase


@dataclass
class Group(MongoBase):
    chat_id: int  # TELEGRAM ID
    name: str
    silent: bool = False

    def __post_init__(self):
        super().__post_init__()

        # CHAT ID
        if not isinstance(self.chat_id, int):
            e = f"O chat_id precisa ser do tipo int ({type(self.chat_id)})."
            raise TypeError(e)

        # NAME
        if not isinstance(self.name, str):
            e = f"O name precisa ser do tipo str ({type(self.name)})."
            raise TypeError(e)

        # SILENT
        if not isinstance(self.silent, bool):
            e = f"O silent precisa ser do tipo bool ({type(self.silent)})."
            raise TypeError(e)

    def __eq__(self, value):
        result = False
        if isinstance(value, Group):
            result = self.chat_id == value.chat_id
        elif isinstance(value, str) and value.isnumeric():
            result = self.chat_id == int(value)
        elif isinstance(value, int):
            result = self.chat_id == value

        return result

    @property
    def telegram_text(self) -> str:
        text = f"Grupo: {self.name}\n"
        text += f"ID do Grupo: {self.chat_id}\n"
        text += f"Modo Silencioso: {self.translate(self.silent)}\n"

        return text


if __name__ == "__main__":
    print(" START LOCAL TEST ".center(79, "="))
    group = Group(chat_id=123456789, name="Teste")

    print("\nGROUP:")
    print(group)

    print("\nGROUP.TELEGRAM_TEXT:")
    print(group.telegram_text)

    print(" END LOCAL TEST ".center(79, "="))
