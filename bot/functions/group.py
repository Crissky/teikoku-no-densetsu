from bot.constants.section import GROUP_SECTION_NAME, GROUP_SUBSECTION_NAME
from bot.functions.text import create_telegram_text
from teikoku.register.group import Group


def group_telegram_text(
    group: Group,
    section_name: str = GROUP_SECTION_NAME,
    subsection_name: str = GROUP_SUBSECTION_NAME,
    use_emoji: bool = True,
) -> str:
    """Retorna uma string formatada com os dados de group."""

    return create_telegram_text(
        obj=group,
        section_name=section_name,
        subsection_name=subsection_name,
        use_emoji=use_emoji,
    )
