import unittest
from teikoku.world.coor import Coordinate


class TestCoordinate(unittest.TestCase):

    def _make_coordinate(self, x=0, y=0):
        """Cria e retorna uma instância de Coordinate com valores padrão."""

        return Coordinate(x=x, y=y)

    def test_show(self):
        """Verifica se show retorna a representação correta da coordenada."""

        coord = self._make_coordinate(x=3, y=7)
        self.assertEqual(coord.show, "(3, 7)")

    def test_x_valid(self):
        """Verifica se x válido é aceito sem alterações."""

        coord = self._make_coordinate(x=10)
        self.assertEqual(coord.x, 10)

    def test_y_valid(self):
        """Verifica se y válido é aceito sem alterações."""

        coord = self._make_coordinate(y=20)
        self.assertEqual(coord.y, 20)

    def test_x_invalid_type_raises_type_error(self):
        """Verifica se x de tipo inválido levanta TypeError."""

        with self.assertRaises(TypeError):
            self._make_coordinate(x="1")

    def test_y_invalid_type_raises_type_error(self):
        """Verifica se y de tipo inválido levanta TypeError."""

        with self.assertRaises(TypeError):
            self._make_coordinate(y="1")

    def test_x_float_raises_type_error(self):
        """Verifica se x do tipo float levanta TypeError."""

        with self.assertRaises(TypeError):
            self._make_coordinate(x=1.0)

    def test_y_float_raises_type_error(self):
        """Verifica se y do tipo float levanta TypeError."""

        with self.assertRaises(TypeError):
            self._make_coordinate(y=1.0)

    def test_x_negative_valid(self):
        """Verifica se x negativo é aceito sem alterações."""

        coord = self._make_coordinate(x=-5)
        self.assertEqual(coord.x, -5)

    def test_y_negative_valid(self):
        """Verifica se y negativo é aceito sem alterações."""

        coord = self._make_coordinate(y=-5)
        self.assertEqual(coord.y, -5)

    def test_x_zero_valid(self):
        """Verifica se x igual a zero é aceito sem alterações."""

        coord = self._make_coordinate(x=0)
        self.assertEqual(coord.x, 0)

    def test_y_zero_valid(self):
        """Verifica se y igual a zero é aceito sem alterações."""

        coord = self._make_coordinate(y=0)
        self.assertEqual(coord.y, 0)
