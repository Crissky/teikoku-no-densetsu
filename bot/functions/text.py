from general.enums.emojis import get_random_face_emoji
from general.functions.text import create_text_in_box, format_subsection
from repository.mongo.base import MongoBase


def create_telegram_text(
    obj: MongoBase,
    section_name: str,
    subsection_name: str,
    previous_text: str = None,
    next_text: str = None,
    use_emoji: bool = True,
) -> str:
    """Retorna uma string formatada com os dados de obj (MongoBase)."""

    telegram_text = obj.telegram_text
    subsection = format_subsection(text=subsection_name)
    telegram_text = f"{subsection}" f"{telegram_text}"

    if isinstance(previous_text, str) is True:
        telegram_text = f"{previous_text}\n\n{telegram_text}"
    if isinstance(next_text, str) is True:
        telegram_text = f"{telegram_text}\n\n{next_text}"

    telegram_text = create_text_in_box(
        text=telegram_text, section_name=section_name, use_emoji=use_emoji
    )

    return telegram_text
