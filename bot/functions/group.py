from bot.constants.message import GROUP_NOT_FOUND_ERROR
from bot.constants.section import (
    GROUP_SECTION_NAME,
    GROUP_SUBSECTION_NAME,
    NOT_FOUND_GROUP_SECTION_NAME,
)
from bot.functions.text import create_telegram_text, create_text_in_box
from teikoku.entity.register.group import Group


def group_telegram_text(
    group: Group,
    chat_id: int,
    section_name: str = GROUP_SECTION_NAME,
    subsection_name: str = GROUP_SUBSECTION_NAME,
    use_emoji: bool = True,
) -> str:
    """Retorna uma string formatada com os dados de group."""

    if group is None:
        telegram_text = GROUP_NOT_FOUND_ERROR.format(id=chat_id)
        telegram_text = create_text_in_box(
            text=telegram_text, section_name=NOT_FOUND_GROUP_SECTION_NAME
        )
    else:
        telegram_text = create_telegram_text(
            obj=group,
            section_name=section_name,
            subsection_name=subsection_name,
            use_emoji=use_emoji,
        )

    return telegram_text
