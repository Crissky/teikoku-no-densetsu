import logging

from typing import Any, Iterable, Optional, Tuple, get_type_hints

from telegram import Update
from telegram.ext import CallbackContext

from repository.mongo.models.world import WorldModel
from teikoku.entity.world.world import World

logger = logging.getLogger(__name__)


def save_world(world: World) -> World:
    """Salva um world no banco de dados e retorna o world recuperado.

    Persiste um objeto World no banco de dados através do WorldModel e
    em seguida recupera o world salvo para confirmar a operação.

    Args:
        world: Objeto World a ser salvo no banco de dados.

    Returns:
        World: Objeto World recuperado do banco de dados após o salvamento.

    Raises:
        TypeError: Se world não for do tipo World.
    """

    if not isinstance(world, World):
        raise TypeError(f"world precisa ser do tipo World ({type(world)}).")

    world_model = WorldModel()
    world_model.save(world)
    retrieved_world = get_world_by_chat_id(world.chat_id)
    logger.info(
        f"World {retrieved_world.name}' salvo com "
        f"CHAT ID '{retrieved_world.chat_id}'"
    )

    return retrieved_world


def update_world(
    args: Iterable[Tuple[str, Any]],
    world: Optional[World] = None,
    update: Optional[Update] = None,
) -> Optional[World]:
    """Atualiza os atributos do world com os valores passados em args.
    args deve ser um iterável de tuplas no formato (atributo, valor).
    Exemplo: [("level", 10), ("hp", 200)]
    """


def get_world_by_chat_id(chat_id: int) -> World:
    """Recupera um world do banco de dados pelo ID do chat.

    Args:
        chat_id: ID do chat do Telegram associado ao world.

    Returns:
        World: Objeto World correspondente ao chat_id fornecido.

    Raises:
        TypeError: Se chat_id não for do tipo int.
    """

    if not isinstance(chat_id, int):
        raise TypeError(f"chat_id precisa ser um int ({type(chat_id)}).")

    world_model = WorldModel()
    query = {"chat_id": chat_id}
    world = world_model.get(query=query)

    return world


def get_world(
    update: Optional[Update] = None,
    context: Optional[CallbackContext] = None,
) -> World:
    """Recupera um world a partir de um Update ou CallbackContext do Telegram.

    Extrai o chat_id do objeto Update ou CallbackContext fornecido e busca
    o world correspondente no banco de dados.

    Args:
        update: Objeto Update do Telegram contendo informações da mensagem.
        context: Objeto CallbackContext do Telegram contendo o contexto da
            callback.

    Returns:
        World: Objeto World correspondente ao chat_id extraído.

    Raises:
        ValueError: Se nem update nem context forem fornecidos.
    """

    if isinstance(update, Update):
        chat_id = update.effective_chat.id
    elif isinstance(context, CallbackContext):
        chat_id = context._chat_id
    else:
        raise ValueError("É preciso informar ou update ou context.")

    return get_world_by_chat_id(chat_id)


def exists_world(
    chat_id: Optional[int] = None,
    update: Optional[Update] = None,
    context: Optional[CallbackContext] = None,
) -> bool:
    """Verifica se existe um world no banco de dados.

    Pode verificar a existência usando diretamente um chat_id ou extraindo-o
    de um objeto Update ou CallbackContext do Telegram.

    Args:
        chat_id: ID do chat do Telegram a ser verificado.
        update: Objeto Update do Telegram para extrair o chat_id.
        context: Objeto CallbackContext do Telegram para extrair o chat_id.

    Returns:
        bool: True se o world existe, False caso contrário.

    Raises:
        TypeError: Se chat_id não for do tipo int após extração.
    """

    if isinstance(update, Update) and chat_id is None:
        chat_id = update.effective_chat.id
    elif isinstance(context, CallbackContext) and chat_id is None:
        chat_id = context._chat_id
    if not isinstance(chat_id, int):
        raise TypeError("chat_id precisa ser um int.")
    world_model = WorldModel()

    return world_model.exists(_id=chat_id)
