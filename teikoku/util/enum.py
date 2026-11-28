from enum import Enum


def try_enum(enum_class: Enum, value: str):
    """ Tenta converter um valor em um Enum. Se não conseguir, retorna None.
    """

    if not isinstance(enum_class, Enum):
        ec_type = type(enum_class)
        TypeError(f"enum_class deve ser do tipo Enum. Tipo: {ec_type}.")
    if not isinstance(value, str):
        value_type = type(value)
        TypeError(f"value deve ser do tipo str. Tipo: {value_type}.")
    try:
        return enum_class(value)
    except ValueError:
        return enum_class.__members__.get(value)
