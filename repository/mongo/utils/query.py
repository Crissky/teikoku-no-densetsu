from repository.mongo.utils.field import QueryField


class Query:
    def __init__(self, *query_fields: QueryField):
        self.query_fields = query_fields

    @property
    def query(self) -> dict:
        query = {}
        for qf in self.query_fields:
            if qf.field in query:
                raise ValueError(f"Campo '{qf.field}' duplicado.")
            query.update(qf.query)

        return query
