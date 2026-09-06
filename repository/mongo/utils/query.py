from typing import Any

from repository.mongo.utils.field import QueryField


class Query:
    def __init__(self, *query_fields: QueryField):
        self.query_fields = query_fields

    def __iter__(self):
        return iter(self.query_fields)

    def __str__(self):
        text = ", ".join((str(qf) for qf in self))
        return f"[{text}]"

    def __repr__(self):
        text = ", ".join((repr(qf) for qf in self))
        return f"{self.__class__.__name__}([{text}])"

    def load_values(self, obj: Any):
        for qf in self.query_fields:
            qf.load_value(obj)

    @property
    def query(self) -> dict:
        query = {}
        for qf in self.query_fields:
            if qf.field in query:
                raise ValueError(f"Campo {qf.field!r} duplicado.")
            query.update(qf.query)

        return query


if __name__ == "__main__":
    print(" START LOCAL TEST ".center(79, "="))

    qf1 = QueryField("test", 123, int)
    qf2 = QueryField("test2", "abc", str)
    q = Query(qf1, qf2)
    print("STR:", q)
    print("REPR:", repr(q))
    print("QUERY:", q.query)

    print(" END LOCAL TEST ".center(79, "="))
