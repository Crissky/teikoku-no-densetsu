from dataclasses import dataclass

from repository.mongo.base import MongoBase


@dataclass
class Group(MongoBase):
    chat_id: int  # TELEGRAM ID
    name: str
    silent: bool = False

    UPDATABLE_ATTR_LIST = ("silent",)

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
        text = f"*Grupo*: {self.name}\n"
        text += f"*ID do Grupo*: {self.chat_id}\n"
        text += f"*Modo Silencioso*: {self.translate(self.silent)}\n"

        return text


if __name__ == "__main__":
    print(" START LOCAL TEST ".center(79, "="))
    print(f"UPDATABLE_ATTR_LIST: {Group.UPDATABLE_ATTR_LIST}")
    group = Group(chat_id=123456789, name="Grupo Teste")

    print("\nGROUP:")
    print(group)

    print("\nGROUP.TELEGRAM_TEXT:")
    print(group.telegram_text)

    print("\nGROUP.TO_DICT:")
    print(group.to_dict())

    print(" END LOCAL TEST ".center(79, "="))
