import unittest
from enum import Enum

from repository.mongo.utils.field import QueryField


class SampleEnum(Enum):
    NAME = "name"
    AGE = "age"


class DummyObj:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class TestQueryFieldInit(unittest.TestCase):

    def test_field_from_string(self):
        qf = QueryField("name")
        self.assertEqual(qf.field, "name")

    def test_field_from_enum(self):
        qf = QueryField(SampleEnum.NAME)
        self.assertEqual(qf.field, "name")

    def test_value_stored(self):
        qf = QueryField("name", "Alice")
        self.assertEqual(qf.value, "Alice")

    def test_value_type_stored(self):
        qf = QueryField("age", 10, int)
        self.assertEqual(qf.value_type, int)

    def test_check_value_type_raises(self):
        with self.assertRaises(TypeError):
            QueryField("age", "not_an_int", int)

    def test_check_value_type_passes(self):
        qf = QueryField("age", 5, int)
        self.assertEqual(qf.value, 5)

    def test_no_aliases_defaults_to_empty_tuple(self):
        qf = QueryField("name")
        self.assertEqual(qf.field_aliases, tuple())

    def test_alias_from_string(self):
        qf = QueryField("name", field_aliases="alias")
        self.assertEqual(qf.field_aliases, ("alias",))

    def test_alias_from_enum(self):
        qf = QueryField("name", field_aliases=SampleEnum.AGE)
        self.assertEqual(qf.field_aliases, ("age",))

    def test_alias_from_tuple(self):
        qf = QueryField("name", field_aliases=(SampleEnum.NAME, "alias2"))
        self.assertEqual(qf.field_aliases, ("name", "alias2"))


class TestQueryFieldEquality(unittest.TestCase):

    def test_equal_same_fields(self):
        qf1 = QueryField("name", "Alice", str)
        qf2 = QueryField("name", "Alice", str)
        self.assertEqual(qf1, qf2)

    def test_not_equal_different_value(self):
        self.assertNotEqual(
            QueryField("name", "Alice"), QueryField("name", "Bob")
        )

    def test_not_equal_non_queryfield(self):
        self.assertNotEqual(QueryField("name"), "name")


class TestQueryFieldHelpers(unittest.TestCase):

    def setUp(self):
        self.qf = QueryField("name", "Alice", str)

    def test_equal_field_true(self):
        self.assertTrue(self.qf.equal_field("name"))

    def test_equal_field_enum(self):
        self.assertTrue(self.qf.equal_field(SampleEnum.NAME))

    def test_equal_field_false(self):
        self.assertFalse(self.qf.equal_field("other"))

    def test_equal_value_true(self):
        self.assertTrue(self.qf.equal_value("Alice"))

    def test_equal_value_false(self):
        self.assertFalse(self.qf.equal_value("Bob"))

    def test_equal_value_type_true(self):
        self.assertTrue(self.qf.equal_value_type(str))

    def test_equal_value_type_false(self):
        self.assertFalse(self.qf.equal_value_type(int))

    def test_query_property(self):
        self.assertEqual(self.qf.query, {"name": "Alice"})

    def test_clear_value(self):
        self.qf.clear_value()
        self.assertIsNone(self.qf.value)

    def test_str(self):
        self.assertEqual(str(self.qf), "{'name': 'Alice'}")

    def test_repr(self):
        self.assertIn("QueryField", repr(self.qf))


class TestQueryFieldLoadValue(unittest.TestCase):

    def test_load_from_primary_field(self):
        qf = QueryField("name")
        qf.load_value(DummyObj(name="Alice"))
        self.assertEqual(qf.value, "Alice")

    def test_load_from_alias(self):
        qf = QueryField("name", field_aliases="username")
        qf.load_value(DummyObj(username="Bob"))
        self.assertEqual(qf.value, "Bob")

    def test_load_raises_when_no_attr(self):
        qf = QueryField("name")
        with self.assertRaises(AttributeError):
            qf.load_value(DummyObj(other="x"))

    def test_load_prefers_primary_over_alias(self):
        qf = QueryField("name", field_aliases="username")
        qf.load_value(DummyObj(name="Primary", username="Alias"))
        self.assertEqual(qf.value, "Primary")


if __name__ == "__main__":
    unittest.main()
