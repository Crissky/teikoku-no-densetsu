import unittest

from repository.mongo.utils.field import QueryField
from repository.mongo.utils.query import Query


class TestQuery(unittest.TestCase):

    def test_single_field(self):
        q = Query(QueryField("name", "Alice"))
        self.assertEqual(q.query, {"name": "Alice"})

    def test_multiple_fields(self):
        q = Query(QueryField("name", "Alice"), QueryField("age", 30))
        self.assertEqual(q.query, {"name": "Alice", "age": 30})

    def test_empty_query(self):
        q = Query()
        self.assertEqual(q.query, {})

    def test_duplicate_field_raises_value_error(self):
        with self.assertRaises(ValueError):
            Query(QueryField("name", "Alice"), QueryField("name", "Bob")).query

    def test_iter_yields_query_fields(self):
        qf1, qf2 = QueryField("a", 1), QueryField("b", 2)
        q = Query(qf1, qf2)
        self.assertEqual(list(q), [qf1, qf2])

    def test_str_single_field(self):
        q = Query(QueryField("x", 1))
        self.assertEqual(str(q), "[{'x': 1}]")

    def test_str_empty(self):
        self.assertEqual(str(Query()), "[]")

    def test_str_multiple_fields(self):
        q = Query(QueryField("a", 1), QueryField("b", 2))
        self.assertEqual(str(q), "[{'a': 1}, {'b': 2}]")

    def test_repr_format(self):
        q = Query(QueryField("x", 1))
        self.assertEqual(repr(q), "Query([QueryField('x'=1 None)])")

    def test_load_values_updates_fields_from_object(self):
        class Obj:
            name = "Bob"
            age = 25
        q = Query(QueryField("name", None), QueryField("age", None))
        q.load_values(Obj())
        self.assertEqual(q.query, {"name": "Bob", "age": 25})

    def test_load_values_raises_attribute_error_for_missing_field(self):
        q = Query(QueryField("missing", None))
        with self.assertRaises(AttributeError):
            q.load_values(object())
