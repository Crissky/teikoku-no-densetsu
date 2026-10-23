from enum import Enum
from typing import Any, Union

from repository.mongo.models.group import GroupModel
from repository.mongo.models.player import PlayerModel


def get_attribute_group_or_player(_id: Any, field: Union[str, Enum]) -> Any:
    """Retorna o atributo de um group ou player.

    Primeiro tenta recuperar o valor de um grupo usando o ID.
    Se não encontrar, tenta recuperar o valor de um player usando o ID.
    """

    group_model = GroupModel()
    player_model = PlayerModel()
    retrieve_value = None
    if isinstance(field, Enum):
        field = field.value
    if not isinstance(field, str):
        raise TypeError("Field precisa ser do tipo str ou Enum.")

    retrieve_value = group_model.get(_id=_id, field=field)
    if retrieve_value is None:
        retrieve_value = player_model.get(_id=_id, field=field)
    if not isinstance(retrieve_value, (dict, type(None))):
        raise TypeError("O valor retornado não é um dicionário nem None.")

    return (
        retrieve_value.get(field)
        if isinstance(retrieve_value, dict)
        else retrieve_value
    )
