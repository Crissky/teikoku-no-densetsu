import unittest
from teikoku.entity.register.player import Player


class TestPlayer(unittest.TestCase):

    def _make_player(
        self, user_id=123, name="Teste", username=None, silent=False, **kwargs
    ):
        """Cria e retorna uma instância de Player com valores padrão."""

        return Player(
            user_id=user_id,
            name=name,
            username=username,
            silent=silent,
            **kwargs
        )

    def test_user_id_valid(self):
        """Verifica se user_id válido é aceito sem alterações."""

        player = self._make_player(user_id=123456789)
        self.assertEqual(player.user_id, 123456789)

    def test_user_id_invalid_type_raises_type_error(self):
        """Verifica se user_id de tipo inválido levanta TypeError."""

        with self.assertRaises(TypeError):
            self._make_player(user_id="123")

    def test_name_none_raises_type_error(self):
        """Verifica se name igual a None é mantido sem alterações."""

        with self.assertRaises(TypeError):
            self._make_player(name=None)

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

    def test_silent_default_false(self):
        """Verifica se silent tem valor padrão False."""

        player = self._make_player()
        self.assertFalse(player.silent)

    def test_silent_true(self):
        """Verifica se silent=True é aceito."""

        player = self._make_player(silent=True)
        self.assertTrue(player.silent)

    def test_silent_invalid_type_raises_type_error(self):
        """Verifica se silent de tipo inválido levanta TypeError."""

        with self.assertRaises(TypeError):
            self._make_player(silent="true")

    def test_telegram_text_without_username(self):
        """Verifica se telegram_text é formatado corretamente sem username."""

        player = self._make_player(user_id=123, name="Teste")
        expected = (
            "*Nome*: Teste\n*Nome de Usuário*: \n"
            "*ID de Usuário*: 123\n*Modo Silencioso*: Não\n"
        )
        self.assertEqual(player.telegram_text, expected)

    def test_telegram_text_with_username(self):
        """Verifica se telegram_text é formatado corretamente com username."""

        player = self._make_player(
            user_id=123, name="Teste", username="@jogador"
        )
        expected = (
            "*Nome*: Teste\n*Nome de Usuário*: @jogador\n"
            "*ID de Usuário*: 123\n*Modo Silencioso*: Não\n"
        )
        self.assertEqual(player.telegram_text, expected)

    def test_telegram_text_silent_true(self):
        """Verifica se telegram_text exibe 'Sim' quando silent=True."""

        player = self._make_player(user_id=123, name="Teste", silent=True)
        expected = (
            "*Nome*: Teste\n*Nome de Usuário*: \n"
            "*ID de Usuário*: 123\n*Modo Silencioso*: Sim\n"
        )
        self.assertEqual(player.telegram_text, expected)

    def test_effective_name_returns_username_when_set(self):
        """Verifica se effective_name retorna username quando definido."""

        player = self._make_player(username="@jogador")
        self.assertEqual(player.effective_name, "@jogador")

    def test_effective_name_returns_name_when_no_username(self):
        """Verifica se effective_name retorna name quando username é None."""

        player = self._make_player(name="Teste")
        self.assertEqual(player.effective_name, "Teste")

    def test_to_dict_contains_expected_keys(self):
        """Verifica se to_dict retorna as chaves esperadas."""

        player = self._make_player(user_id=123, name="Teste")
        d = player.to_dict()
        self.assertIn("user_id", d)
        self.assertIn("name", d)
        self.assertIn("username", d)
        self.assertIn("silent", d)

    def test_has_updatable_attr_silent(self):
        """Verifica se 'silent' está na lista de atributos atualizáveis."""

        player = self._make_player()
        self.assertTrue(player.has_updatable_attr("silent"))

    def test_has_updatable_attr_invalid(self):
        """Verifica se atributo não atualizável retorna False."""

        player = self._make_player()
        self.assertFalse(player.has_updatable_attr("name"))

    def test_invalid_id_type_raises_type_error(self):
        """Verifica se _id de tipo inválido levanta TypeError."""

        with self.assertRaises(TypeError):
            self._make_player(_id=123)
