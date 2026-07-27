import logging
from typing import Any, Iterable, Optional, Tuple, get_type_hints

from telegram import Update
from telegram.constants import ChatMemberStatus
from telegram.ext import CallbackContext

from repository.mongo.models.player import PlayerModel
from teikoku.entity.register.player import Player

ADMIN_TYPES = (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
logger = logging.getLogger(__name__)


def save_player(player: Player) -> Player:
    """Salva um player no banco de dados e retorna o player recuperado.

    Persiste um objeto Player no banco de dados através do PlayerModel e
    em seguida recupera o player salvo para confirmar a operação.

    Args:
        player: Objeto Player a ser salvo no banco de dados.

    Returns:
        Player: Objeto Player recuperado do banco de dados após o salvamento.

    Raises:
        TypeError: Se player não for do tipo Player.
    """

    if not isinstance(player, Player):
        raise TypeError(f"player precisa ser do tipo Player ({type(player)}).")

    player_model = PlayerModel()
    player_model.save(player)
    retrieved_player = get_player_by_user_id(player.user_id)
    logger.info(
        f"Player '{retrieved_player.name}' salvo com "
        f"USER ID '{retrieved_player.user_id}'"
    )

    return retrieved_player


def update_player(
    args: Iterable[Tuple[str, Any]],
    player: Optional[Player] = None,
    update: Optional[Update] = None,
) -> Optional[Player]:
    """Atualiza os atributos do player com os valores passados em args.
    args deve ser um iterável de tuplas no formato (atributo, valor).

    Args:
        args: Iterável de tuplas no formato (atributo, valor) para atualização.
            Exemplo: [("name", "João"), ("username", "@joaozinho")]
        player: Objeto Player a ser atualizado. Se None, tenta recuperar do
            banco.
        update: Objeto Update do Telegram para obter o player se player=None.

    Returns:
        Optional[Player]: Objeto Player atualizado, ou None se não houve
            atualização.

    Raises:
        TypeError: Se player não for do tipo Player.
        ValueError: Se nem update nem player forem fornecidos.
    """

    if isinstance(update, Update) and player is None:
        player = get_player(update=update)

    if not isinstance(player, Player):
        raise TypeError(f"player precisa ser do tipo Player ({type(player)}).")

    is_updated = False
    retrieved_player = None
    player_type_hints = get_type_hints(player)
    for attr, value in args:
        if player.has_updatable_attr(attr):
            player_attr_type = player_type_hints[attr]
            if player_attr_type == type(value):
                setattr(player, attr, value)
                is_updated = True
            else:
                logger.warning(
                    f"O atributo '{attr}' não pode ser atualizado com o valor "
                    f"do tipo {type(value)}, pois o tipo esperado é "
                    f"{type(player_attr_type)}."
                )
        else:
            logger.warning(
                f"Player não possui ou não pode alterar o atributo '{attr}'."
            )

    if is_updated:
        player_model = PlayerModel()
        player_model.save(player)
        retrieved_player = get_player_by_user_id(player.user_id)

        return retrieved_player


def get_player_by_user_id(user_id: int) -> Player:
    """Recupera um player do banco de dados pelo ID do chat.

    Args:
        user_id: ID do chat do Telegram associado ao player.

    Returns:
        Player: Objeto Player correspondente ao user_id fornecido.

    Raises:
        TypeError: Se user_id não for do tipo int.
    """

    if not isinstance(user_id, int):
        raise TypeError(f"user_id precisa ser um int ({type(user_id)}).")

    player_model = PlayerModel()
    query = {"user_id": user_id}
    player = player_model.get(query=query)

    return player


def get_player(
    update: Optional[Update] = None,
    context: Optional[CallbackContext] = None,
) -> Player:
    """Recupera um player a partir de um Update ou CallbackContext do Telegram.

    Extrai o user_id do objeto Update ou CallbackContext fornecido e busca
    o player correspondente no banco de dados.

    Args:
        update: Objeto Update do Telegram contendo informações da mensagem.
        context: Objeto CallbackContext do Telegram contendo o contexto da
            callback.

    Returns:
        Player: Objeto Player correspondente ao user_id extraído.

    Raises:
        ValueError: Se nem update nem context forem fornecidos.
    """

    if isinstance(update, Update):
        user_id = update.effective_user.id
    elif isinstance(context, CallbackContext):
        user_id = context._user_id
    else:
        raise ValueError("É preciso informar ou update ou context.")

    return get_player_by_user_id(user_id)


def exists_player(
    user_id: Optional[int] = None,
    update: Optional[Update] = None,
    context: Optional[CallbackContext] = None,
) -> bool:
    """Verifica se existe um player no banco de dados.

    Pode verificar a existência usando diretamente um user_id ou extraindo-o
    de um objeto Update ou CallbackContext do Telegram.

    Args:
        user_id: ID do chat do Telegram a ser verificado.
        update: Objeto Update do Telegram para extrair o user_id.
        context: Objeto CallbackContext do Telegram para extrair o user_id.

    Returns:
        bool: True se o player existe, False caso contrário.

    Raises:
        TypeError: Se user_id não for do tipo int após extração.
    """

    if isinstance(update, Update) and user_id is None:
        user_id = update.effective_user.id
    elif isinstance(context, CallbackContext) and user_id is None:
        user_id = context._user_id
    if not isinstance(user_id, int):
        raise TypeError("user_id precisa ser um int.")
    player_model = PlayerModel()

    return player_model.exists(_id=user_id)


async def user_is_admin(update: Update) -> bool:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    chat_member = await update._bot.get_chat_member(
        chat_id=chat_id, user_id=user_id
    )

    return chat_member.status in ADMIN_TYPES
