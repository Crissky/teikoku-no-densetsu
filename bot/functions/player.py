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
    previous_text: str = None,
    next_text: str = None,
    player_not_found_msg: str = None,
    use_emoji: bool = True,
) -> str:
    """Retorna uma string formatada com os dados de player."""

    if player is None:
        if player_not_found_msg:
            telegram_text = player_not_found_msg
        else:
            telegram_text = PLAYER_NOT_FOUND_ERROR

        telegram_text = telegram_text.format(id=user_id)
        telegram_text = create_text_in_box(
            text=telegram_text, section_name=NOT_FOUND_PLAYER_SECTION_NAME
        )
    else:
        telegram_text = create_telegram_text(
            obj=player,
            section_name=section_name,
            subsection_name=subsection_name,
            previous_text=previous_text,
            next_text=next_text,
            use_emoji=use_emoji,
        )

    return telegram_text
