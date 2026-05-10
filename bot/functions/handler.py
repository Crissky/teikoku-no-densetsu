import re
from typing import Callable


def check_pattern(
    pattern: str,
    regex: bool = False,
    _case: bool = True,
    _match: bool = True,
) -> Callable:
    """Verifica se uma string corresponde a um padrão.

    Se regex for True, o padrão será tratado como uma expressão regular.
    Se case for True, a comparação será case sensitive.
    Se _match for True, a comparação será feita com match (ou com `==`),
    caso contrário, será feita com search (ou com `in`).
    """

    def check(data: str) -> bool:
        if regex:
            flags = 0 if _case else re.IGNORECASE
            fn = re.match if _match else re.search
            return bool(fn(pattern, data, flags))
        else:
            p, d = (
                (pattern, data) if _case else (pattern.upper(), data.upper())
            )
            return p == d if _match else p in d

    return check
