from bot.constants.message import PLAYER_NOT_FOUND_ERROR
from bot.constants.section import (
    NOT_FOUND_PLAYER_SECTION_NAME,
    PLAYER_SECTION_NAME,
    PLAYER_SUBSECTION_NAME,
)
from bot.functions.text import create_telegram_text, create_text_in_box
from teikoku.entity.register.player import Player


def player_telegram_text(
    player: Player,
    user_id: int,
    section_name: str = PLAYER_SECTION_NAME,
    subsection_name: str = PLAYER_SUBSECTION_NAME,
    use_emoji: bool = True,
) -> str:
    """Retorna uma string formatada com os dados de player."""

    if player is None:
        telegram_text = PLAYER_NOT_FOUND_ERROR.format(id=user_id)
        telegram_text = create_text_in_box(
            text=telegram_text, section_name=NOT_FOUND_PLAYER_SECTION_NAME
        )
    else:
        telegram_text = create_telegram_text(
            obj=player,
            section_name=section_name,
            subsection_name=subsection_name,
            use_emoji=use_emoji,
        )

    return telegram_text
