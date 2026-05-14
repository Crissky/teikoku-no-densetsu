import logging

import re
from typing import Any, List, Tuple

logger = logging.getLogger(__name__)


def format_args(args: List[str]) -> List[Tuple[str, str]]:
    args_list = []
    for arg in args:
        if "=" in arg:
            key, value = arg.split("=", 1)
            value = parse_string(value)
            args_list.append((key, value))
        else:
            logger.warning(f"'{arg}' não está no formato chave=valor.")

    return args_list


def parse_string(value: str) -> Any:
    if re.match(r"^(true|sim)$", value, flags=re.IGNORECASE):
        value = True
    elif re.match(r"^(false|n[ãa]o)$", value, flags=re.IGNORECASE):
        value = False
    elif re.match(r"^-?\d+\.\d+$", value):
        value = float(value)
    elif re.match(r"^-?\d+$", value):
        value = int(value)
    else:
        logger.warning(f"Valor '{value}' não é um tipo primitivo válido.")

    return value
