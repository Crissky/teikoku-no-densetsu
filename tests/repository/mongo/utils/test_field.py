import unittest
from enum import Enum

from repository.mongo.utils.field import QueryField


class SampleEnum(Enum):
    NAME = "sample_name"


class TestQueryField(unittest.TestCase):

    def test_plain_string_field(self):
        qf = QueryField("name", "Alice")
        self.assertEqual(qf.field, "name")

    def test_enum_field_extracts_value(self):
        qf = QueryField(SampleEnum.NAME, "Alice")
        self.assertEqual(qf.field, "sample_name")

    def test_no_type_check_accepts_any_value(self):
        qf = QueryField("score", 42)
        self.assertEqual(qf.value, 42)

    def test_valid_type_check_passes(self):
        qf = QueryField("score", 42, int)
        self.assertEqual(qf.value, 42)

    def test_invalid_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            QueryField("score", "not_an_int", int)

    def test_query_property(self):
        qf = QueryField("level", 5, int)
        self.assertEqual(qf.query, {"level": 5})

    def test_load_value_sets_value_from_object(self):
        class Obj:
            score = 99
        qf = QueryField("score", None)
        qf.load_value(Obj())
        self.assertEqual(qf.value, 99)

    def test_load_value_raises_attribute_error_for_missing_field(self):
        qf = QueryField("missing", None)
        with self.assertRaises(AttributeError):
            qf.load_value(object())

