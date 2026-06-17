from typing import Any, Iterable, Optional, Tuple

from telegram import Update
from telegram.ext import ContextTypes

from repository.mongo.models.world import WorldModel
from teikoku.entity.world.world import World
import logging

logger = logging.getLogger(__name__)


def save_world(world: World) -> World:
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
    if not isinstance(chat_id, int):
        raise TypeError(f"chat_id precisa ser um int ({type(chat_id)}).")

    world_model = WorldModel()
    query = {"chat_id": chat_id}
    world = world_model.get(query=query)

    return world


def get_world(
    update: Optional[Update] = None,
    context: Optional[ContextTypes.DEFAULT_TYPE] = None,
) -> World:
    if isinstance(update, Update):
        chat_id = update.effective_chat.id
    elif isinstance(context, ContextTypes.DEFAULT_TYPE):
        chat_id = context._chat_id
    else:
        raise ValueError("É preciso informar ou update ou context.")

    return get_world_by_chat_id(chat_id)


def exists_world(
    chat_id: Optional[int] = None,
    update: Optional[Update] = None,
    context: Optional[ContextTypes.DEFAULT_TYPE] = None,
) -> bool:
    if isinstance(update, Update) and chat_id is None:
        chat_id = update.effective_chat.id
    elif isinstance(context, ContextTypes.DEFAULT_TYPE) and chat_id is None:
        chat_id = context._chat_id
    if not isinstance(chat_id, int):
        raise TypeError("chat_id precisa ser um int.")
    world_model = WorldModel()

    return world_model.exists(_id=chat_id)
