from bot.constants.message import PLAYER_NOT_FOUND_ERROR
from bot.constants.section import (
    NOT_FOUND_PLAYER_SECTION_NAME,
    PLAYER_SECTION_NAME,
    PLAYER_SUBSECTION_NAME,
)
from bot.functions.text import create_telegram_text, create_text_in_box
from repository.mongo.functions.player import get_player_attribute_by_id
from teikoku.entity.register.player import Player
from teikoku.enum.register import PlayerAttrEnum


def player_telegram_text(
    player: Player,
    user_id: int,
    section_name: str = None,
    subsection_name: str = None,
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
        if not isinstance(section_name, str):
            section_name = NOT_FOUND_PLAYER_SECTION_NAME

        telegram_text = telegram_text.format(id=user_id)
        telegram_text = create_text_in_box(
            text=telegram_text, section_name=section_name
        )
    else:
        if not isinstance(section_name, str):
            section_name = PLAYER_SECTION_NAME
        if not isinstance(subsection_name, str):
            subsection_name = PLAYER_SUBSECTION_NAME

        telegram_text = create_telegram_text(
            obj=player,
            section_name=section_name,
            subsection_name=subsection_name,
            previous_text=previous_text,
            next_text=next_text,
            use_emoji=use_emoji,
        )

    return telegram_text


# TODO Adicionar a chamada dessa função em "call_telegram_message_function"
# para definir se a mensagem será enviada ou não
def allow_private_messages(user_id) -> bool:
    allow_private_messages_field = PlayerAttrEnum.ALLOW_PRIVATE_MESSAGES.value
    allow_private_messages = get_player_attribute_by_id(
        user_id=user_id, field=allow_private_messages_field
    )

    if isinstance(allow_private_messages, bool):
        return allow_private_messages
    else:
        class_name = Player.__name__
        raise TypeError(
            f"O campo de {class_name} '{allow_private_messages_field}' "
            f"deve ser do tipo 'bool', não '{type(allow_private_messages)}'."
        )
