import unittest

from teikoku.enum.terrain import (
    TerrainColorEnum,
    TerrainNumberEnum,
    TerrainTextEnum,
)


class TestTerrainEnum(unittest.TestCase):

    def test_terrain_number_enum_names_in_color_enum(self):
        tne_names = {e.name for e in TerrainNumberEnum}
        tce_names = {e.name for e in TerrainColorEnum}
        self.assertEqual(tne_names, tce_names)

    def test_terrain_number_enum_names_in_text_enum(self):
        tne_names = {e.name for e in TerrainNumberEnum}
        tte_names = {e.name for e in TerrainTextEnum}
        self.assertEqual(tte_names, tne_names)

    def test_terrain_color_enum_names_in_text_enum(self):
        tce_names = {e.name for e in TerrainColorEnum}
        tte_names = {e.name for e in TerrainTextEnum}
        self.assertEqual(tte_names, tce_names)
