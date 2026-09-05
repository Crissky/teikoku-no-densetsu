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
