import unittest

from teikoku.enum.terrain import TerrainColorsEnum, TerrainValueEnum


class TestTerrainEnum(unittest.TestCase):

    def test_terrain_enum_names_in_colors_enum(self):
        terrain_names = {e.name for e in TerrainValueEnum}
        color_names = {e.name for e in TerrainColorsEnum}
        self.assertEqual(terrain_names, color_names)

    def test_terrain_colors_enum_names_in_terrain_enum(self):
        color_names = {e.name for e in TerrainColorsEnum}
        terrain_names = {e.name for e in TerrainValueEnum}
        self.assertEqual(color_names, terrain_names)
