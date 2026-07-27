import logging

from typing import Any, Iterable, Optional, Tuple, get_type_hints

from telegram import Update
from telegram.ext import CallbackContext

from repository.mongo.models.city import CityModel
from teikoku.entity.city.city_base import City

logger = logging.getLogger(__name__)


def save_city(city: City) -> City:
    """Salva um city no banco de dados e retorna o city recuperado.

    Persiste um objeto City no banco de dados através do CityModel e
    em seguida recupera o city salvo para confirmar a operação.

    Args:
        city: Objeto City a ser salvo no banco de dados.

    Returns:
        City: Objeto City recuperado do banco de dados após o salvamento.

    Raises:
        TypeError: Se city não for do tipo City.
    """

    if not isinstance(city, City):
        raise TypeError(f"city precisa ser do tipo City ({type(city)}).")

    city_model = CityModel()
    city_model.save(city)
    retrieved_city = get_city_by_chat_id(city.chat_id)
    logger.info(
        f"City {retrieved_city.name}' salvo com "
        f"CHAT ID '{retrieved_city.chat_id}'"
    )

    return retrieved_city


def update_city(
    args: Iterable[Tuple[str, Any]],
    city: Optional[City] = None,
    update: Optional[Update] = None,
) -> Optional[City]:
    """Atualiza os atributos do city com os valores passados em args.
    args deve ser um iterável de tuplas no formato (atributo, valor).

    Args:
        args: Iterável de tuplas no formato (atributo, valor) para atualização.
            Exemplo: [("level", 10), ("hp", 200)]
        city: Objeto City a ser atualizado. Se None, tenta recuperar do
            banco.
        update: Objeto Update do Telegram para obter o city se city=None.

    Returns:
        Optional[City]: Objeto City atualizado, ou None se não houve
            atualização.

    Raises:
        TypeError: Se city não for do tipo City.
        ValueError: Se nem update nem city forem fornecidos.
    """

    if isinstance(update, Update) and city is None:
        city = get_city(update=update)

    if not isinstance(city, City):
        raise TypeError(f"city precisa ser do tipo City ({type(city)}).")

    is_updated = False
    retrieved_city = None
    city_type_hints = get_type_hints(city)
    for attr, value in args:
        if city.has_updatable_attr(attr):
            city_attr_type = city_type_hints[attr]
            if city_attr_type == type(value):
                setattr(city, attr, value)
                is_updated = True
            else:
                logger.warning(
                    f"O atributo '{attr}' não pode ser atualizado com o valor "
                    f"do tipo {type(value)}, pois o tipo esperado é "
                    f"{type(city_attr_type)}."
                )
        else:
            logger.warning(
                f"City não possui ou não pode alterar o atributo '{attr}'."
            )

    if is_updated:
        city_model = CityModel()
        city_model.save(city)
        retrieved_city = get_city_by_chat_id(city.chat_id)

        return retrieved_city


def get_city_by_chat_id(chat_id: int) -> City:
    """Recupera um city do banco de dados pelo ID do chat.

    Args:
        chat_id: ID do chat do Telegram associado ao city.

    Returns:
        City: Objeto City correspondente ao chat_id fornecido.

    Raises:
        TypeError: Se chat_id não for do tipo int.
    """

    if not isinstance(chat_id, int):
        raise TypeError(f"chat_id precisa ser um int ({type(chat_id)}).")

    city_model = CityModel()
    query = {"chat_id": chat_id}
    city = city_model.get(query=query)

    return city


def get_city(
    update: Optional[Update] = None,
    context: Optional[CallbackContext] = None,
) -> City:
    """Recupera um city a partir de um Update ou CallbackContext do Telegram.

    Extrai o chat_id do objeto Update ou CallbackContext fornecido e busca
    o city correspondente no banco de dados.

    Args:
        update: Objeto Update do Telegram contendo informações da mensagem.
        context: Objeto CallbackContext do Telegram contendo o contexto da
            callback.

    Returns:
        City: Objeto City correspondente ao chat_id extraído.

    Raises:
        ValueError: Se nem update nem context forem fornecidos.
    """

    if isinstance(update, Update):
        chat_id = update.effective_chat.id
    elif isinstance(context, CallbackContext):
        chat_id = context._chat_id
    else:
        raise ValueError("É preciso informar ou update ou context.")

    return get_city_by_chat_id(chat_id)


def exists_city(
    chat_id: Optional[int] = None,
    update: Optional[Update] = None,
    context: Optional[CallbackContext] = None,
) -> bool:
    """Verifica se existe um city no banco de dados.

    Pode verificar a existência usando diretamente um chat_id ou extraindo-o
    de um objeto Update ou CallbackContext do Telegram.

    Args:
        chat_id: ID do chat do Telegram a ser verificado.
        update: Objeto Update do Telegram para extrair o chat_id.
        context: Objeto CallbackContext do Telegram para extrair o chat_id.

    Returns:
        bool: True se o city existe, False caso contrário.

    Raises:
        TypeError: Se chat_id não for do tipo int após extração.
    """

    if isinstance(update, Update) and chat_id is None:
        chat_id = update.effective_chat.id
    elif isinstance(context, CallbackContext) and chat_id is None:
        chat_id = context._chat_id
    if not isinstance(chat_id, int):
        raise TypeError("chat_id precisa ser um int.")
    city_model = CityModel()

    return city_model.exists(_id=chat_id)
