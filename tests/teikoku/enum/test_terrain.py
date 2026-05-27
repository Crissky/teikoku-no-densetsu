import unittest

from teikoku.enum.terrain import TerrainColorsEnum, TerrainEnum


class TestTerrainEnum(unittest.TestCase):

    def test_terrain_enum_names_in_colors_enum(self):
        terrain_names = {e.name for e in TerrainEnum}
        color_names = {e.name for e in TerrainColorsEnum}
        self.assertEqual(terrain_names, color_names)

    def test_terrain_colors_enum_names_in_terrain_enum(self):
        color_names = {e.name for e in TerrainColorsEnum}
        terrain_names = {e.name for e in TerrainEnum}
        self.assertEqual(color_names, terrain_names)
