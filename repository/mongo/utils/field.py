from enum import Enum
from typing import Any, Type, Union


class QueryField:
    def __init__(
        self,
        field: Union[str, Enum],
        value: Any = None,
        value_type: Type[Any] = None,
    ):
        self.field = field.value if isinstance(field, Enum) else str(field)
        self.value = value
        self.value_type = value_type
        self.check_value_type()

    def __str__(self):
        return f"{{{self.field!r}: {self.value!r}}}"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"({self.field!r}={self.value!r} {self.value_type})"
        )

    def check_value_type(self):
        if self.value_type is not None and self.value is not None:
            if not isinstance(self.value, self.value_type):
                raise TypeError(
                    f"Valor do campo {self.field!r} precisa ser do tipo "
                    f"{self.value_type} ({type(self.value)})."
                )

    def load_value(self, obj: Any):
        if not hasattr(obj, self.field):
            raise AttributeError(
                f"Objeto não possui o atributo {self.field!r}."
            )
        else:
            self.value = getattr(obj, self.field)

    def clear_value(self):
        self.value = None

    @property
    def query(self) -> dict:
        return {self.field: self.value}


if __name__ == "__main__":
    print(" START LOCAL TEST ".center(79, "="))

    qf = QueryField("test", 123, int)
    print("STR:", qf)
    print("REPR:", repr(qf))
    print("QUERY:", qf.query)

    print(" END LOCAL TEST ".center(79, "="))
