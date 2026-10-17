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
    """
    Cria um texto formatado para o Telegram a partir de um objeto MongoBase.

    Args:
        obj: Objeto MongoBase contendo os dados a serem formatados
        section_name: Nome da seção principal
        subsection_name: Nome da subseção
        previous_text: Texto opcional adicionado antes do conteúdo principal
        next_text: Texto opcional adicionado após o conteúdo principal
        use_emoji: Se True, adiciona emojis aleatórios ao cabeçalho e rodapé

    Returns:
        str: Texto formatado e estruturado para envio no Telegram

    Example:
        >>> create_telegram_text(obj, "Império", "Personagem", use_emoji=False)
        '*∞ Império ∞*━━━━━━━━\n\n*Personagem ∞*──────────\nNome: Oda Nobunaga\n\n*∞ Império ∞*━━━━━━━━'
    """

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
