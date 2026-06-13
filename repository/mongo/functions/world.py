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


def get_world_by_chat_id(chat_id: int) -> World: ...


def get_world(
    update: Optional[Update] = None,
    context: Optional[ContextTypes.DEFAULT_TYPE] = None,
) -> World: ...


def exists_world(
    chat_id: Optional[int] = None,
    update: Optional[Update] = None,
    context: Optional[ContextTypes.DEFAULT_TYPE] = None,
) -> bool: ...
