import unittest
from teikoku.register.player import Player


class TestPlayer(unittest.TestCase):

    def _make_player(self, user_id=123, name="Teste", username=None):
        """Cria e retorna uma instância de Player com valores padrão."""
        return Player(user_id=user_id, name=name, username=username)

    def test_user_id_valid(self):
        """Verifica se user_id válido é aceito sem alterações."""
        player = self._make_player(user_id=123456789)
        self.assertEqual(player.user_id, 123456789)

    def test_user_id_zero_raises_value_error(self):
        """Verifica se user_id igual a zero levanta ValueError."""
        with self.assertRaises(ValueError):
            self._make_player(user_id=0)

    def test_user_id_invalid_type_raises_type_error(self):
        """Verifica se user_id de tipo inválido levanta TypeError."""
        with self.assertRaises(TypeError):
            self._make_player(user_id="123")

    def test_name_converts_to_str(self):
        """Verifica se name de tipo não-str é convertido para str."""
        player = self._make_player(name=42)
        self.assertEqual(player.name, "42")

    def test_name_none_kept(self):
        """Verifica se name igual a None é mantido sem alterações."""
        player = self._make_player(name=None)
        self.assertIsNone(player.name)

    def test_username_none_kept(self):
        """Verifica se username igual a None é mantido sem alterações."""
        player = self._make_player()
        self.assertIsNone(player.username)

    def test_username_valid(self):
        """Verifica se username válido (começando com '@') é aceito."""
        player = self._make_player(username="@jogador")
        self.assertEqual(player.username, "@jogador")

    def test_username_without_at_raises_value_error(self):
        """Verifica se username sem '@' levanta ValueError."""
        with self.assertRaises(ValueError):
            self._make_player(username="jogador")

    def test_username_invalid_type_raises_type_error(self):
        """Verifica se username de tipo inválido levanta TypeError."""
        with self.assertRaises(TypeError):
            self._make_player(username=123)

    def test_eq_with_player(self):
        """Verifica se dois Players com mesmo user_id são considerados
        iguais."""
        u1 = self._make_player(user_id=123)
        u2 = self._make_player(user_id=123)
        self.assertEqual(u1, u2)

    def test_eq_with_int(self):
        """Verifica se Player é igual a um int com o mesmo user_id."""
        player = self._make_player(user_id=123)
        self.assertEqual(player, 123)

    def test_eq_with_numeric_str(self):
        """Verifica se Player é igual a uma str numérica com o mesmo
        user_id."""
        player = self._make_player(user_id=123)
        self.assertEqual(player, "123")

    def test_eq_different_ids(self):
        """Verifica se dois Players com user_ids diferentes são considerados
        diferentes."""
        u1 = self._make_player(user_id=123)
        u2 = self._make_player(user_id=456)
        self.assertNotEqual(u1, u2)

    def test_eq_unsupported_type_returns_false(self):
        """Verifica se a comparação com tipo não suportado retorna False."""
        player = self._make_player()
        self.assertFalse(player == 1.5)

    def test_telegram_text_without_username(self):
        """Verifica se telegram_text é formatado corretamente sem username."""
        player = self._make_player(user_id=123, name="Teste")
        expected = "Name: Teste\nUsername: \nUser ID: 123\n"
        self.assertEqual(player.telegram_text, expected)

    def test_telegram_text_with_username(self):
        """Verifica se telegram_text é formatado corretamente com username."""
        player = self._make_player(
            user_id=123, name="Teste", username="@jogador"
        )
        expected = "Name: Teste\nUsername: @jogador\nUser ID: 123\n"
        self.assertEqual(player.telegram_text, expected)
