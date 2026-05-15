from general.enums.emojis import get_random_face_emoji
from general.functions.text import create_text_in_box, format_subsection
from repository.mongo.base import MongoBase


def create_telegram_text(
    obj: MongoBase,
    section_name: str,
    subsection_name: str,
    use_emoji: bool = True,
) -> str:
    """Retorna uma string formatada com os dados de obj (MongoBase)."""

    if use_emoji is True:
        emoji = get_random_face_emoji()
        section_name = emoji + section_name + emoji

    telegram_text = obj.telegram_text
    subsection = format_subsection(text=subsection_name)
    telegram_text = f"{subsection}" f"{telegram_text}"
    telegram_text = create_text_in_box(
        text=telegram_text, section_name=section_name
    )

    return telegram_text
