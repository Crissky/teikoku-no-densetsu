from enum import Enum
from typing import Any, List, Type, Union

from repository.mongo.utils.field import QueryField


class Query:
    def __init__(self, *query_fields: QueryField):
        self.query_fields: List[QueryField] = []
        for qf in query_fields:
            if isinstance(qf, QueryField):
                self.add_query_field(query_field=qf)

    def __iter__(self):
        return iter(self.query_fields)

    def __str__(self):
        text = ", ".join((str(qf) for qf in self))
        return f"[{text}]"

    def __repr__(self):
        text = ", ".join(repr(qf) for qf in self.query_fields)
        return f"{self.__class__.__name__}([{text}])"

    def _check_queries(self):
        for qf in self.query_fields:
            qf.check_value_type()
            self.check_duplicate_field(qf)

    def check_duplicate_field(self, query_field: QueryField):
        if (count := self.fields.count(query_field.field)) > 1:
            raise ValueError(
                f"Campo {query_field.field!r} duplicado ({count})."
            )

    def load_values(self, obj: Any):
        for qf in self.query_fields:
            qf.load_value(obj)

    def clear_values(self):
        for qf in self.query_fields:
            qf.clear_value()

    def add_query_field(
        self,
        field: Union[str, Enum] = None,
        value: Any = None,
        value_type: Type[Any] = None,
        query_field: QueryField = None,
    ):
        if isinstance(field, (str, Enum)):
            qf = QueryField(field, value, value_type)
        elif isinstance(query_field, QueryField):
            qf = query_field
        else:
            raise ValueError(
                "É preciso informar field (str | Enum) ou "
                "query_field (QueryField)."
            )

        qf.check_value_type()
        self.check_duplicate_field(qf)
        self.query_fields.append(qf)

    @property
    def query(self) -> dict:
        query = {}
        for qf in self.query_fields:
            self.check_duplicate_field(qf)
            query.update(qf.query)

        return query

    @property
    def fields(self) -> list:
        return [qf.field for qf in self.query_fields]

    @property
    def values(self) -> list:
        return [qf.value for qf in self.query_fields]

    @property
    def value_types(self) -> list:
        return [qf.value_type for qf in self.query_fields]


if __name__ == "__main__":
    print(" START LOCAL TEST ".center(79, "="))

    qf1 = QueryField("test", 123, int)
    qf2 = QueryField("test2", "abc", str)
    q = Query(qf1, qf2)
    print("STR:", q)
    print("REPR:", repr(q))
    print("QUERY:", q.query)

    print(" END LOCAL TEST ".center(79, "="))
