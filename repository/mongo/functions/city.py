from typing import Any, Iterable, Optional, Tuple

from telegram import Update
from telegram.ext import CallbackContext

from teikoku.entity.city.city_base import City


def save_city(city: City) -> City: ...


def update_city(
    args: Iterable[Tuple[str, Any]],
    city: Optional[City] = None,
    update: Optional[Update] = None,
) -> Optional[City]:
    """Atualiza os atributos da city com os valores passados em args.
    args deve ser um iterável de tuplas no formato (atributo, valor).
    Exemplo: [("level", 10), ("hp", 200)]
    """


def get_city_by_chat_id(chat_id: int) -> City: ...


def get_city(
    update: Optional[Update] = None,
    context: Optional[CallbackContext] = None,
) -> City: ...


def exists_city(
    chat_id: Optional[int] = None,
    update: Optional[Update] = None,
    context: Optional[CallbackContext] = None,
) -> bool: ...
