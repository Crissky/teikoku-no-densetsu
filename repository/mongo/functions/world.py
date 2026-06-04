from typing import Any, Iterable, Optional, Tuple

from telegram import Update
from telegram.ext import ContextTypes

from teikoku.entity.world.world import World


def save_world(world: World) -> World: ...


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
