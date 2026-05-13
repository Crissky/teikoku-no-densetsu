from bot.constants.section import PLAYER_SECTION_NAME, PLAYER_SUBSECTION_NAME
from general.enums.emojis import get_random_face_emoji
from general.functions.text import create_text_in_box, format_subsection
from teikoku.register.player import Player


def player_telegram_text(
    player: Player,
    section_name: str = PLAYER_SECTION_NAME,
    subsection_name: str = PLAYER_SUBSECTION_NAME,
    use_emoji: bool = True,
) -> str:
    """Retorna uma string formatada com os dados de player."""

    if use_emoji is True:
        emoji = get_random_face_emoji()
        section_name = emoji + section_name + emoji

    telegram_text = player.telegram_text
    subsection = format_subsection(text=subsection_name)
    telegram_text = f"{subsection}" f"{telegram_text}"
    telegram_text = create_text_in_box(
        text=telegram_text, section_name=section_name
    )

    return telegram_text
