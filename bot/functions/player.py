from bot.constants.section import PLAYER_SECTION_NAME, PLAYER_SUBSECTION_NAME
from bot.functions.text import create_telegram_text
from teikoku.entity.register.player import Player


def player_telegram_text(
    player: Player,
    section_name: str = PLAYER_SECTION_NAME,
    subsection_name: str = PLAYER_SUBSECTION_NAME,
    use_emoji: bool = True,
) -> str:
    """Retorna uma string formatada com os dados de player."""

    return create_telegram_text(
        obj=player,
        section_name=section_name,
        subsection_name=subsection_name,
        use_emoji=use_emoji,
    )
