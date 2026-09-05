from enum import Enum
from typing import Any, Type, Union


class QueryField:
    def __init__(
        self, field: Union[str, Enum], value: Any, value_type: Type[Any] = None
    ):
        self.field = field.value if isinstance(field, Enum) else str(field)
        self.value = value
        self.value_type = value_type
        self.check_value_type()

    def check_value_type(self):
        if self.value_type is not None:
            if not isinstance(self.value, self.value_type):
                raise TypeError(
                    f"Valor do campo '{self.field}' precisa ser do tipo "
                    f"{self.value_type} ({type(self.value)})."
                )

    def load_value(self, obj: Any):
        if not hasattr(obj, self.field):
            raise AttributeError(
                f"Objeto não possui o atributo {self.field!r}."
            )
        else:
            self.value = getattr(obj, self.field)

    @property
    def query(self) -> dict:
        return {self.field: self.value}


if __name__ == "__main__":
    qf = QueryField("test", 123, int)
    print(qf.query)
