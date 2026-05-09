import unittest
from teikoku.user import User


class TestUser(unittest.TestCase):

    def _make_user(self, telegram_id="123", name="Teste"):
        """Cria e retorna uma instância de User com valores padrão."""

        return User(telegram_id=telegram_id, name=name)

    def test_telegram_id_int_converts_to_str(self):
        """Verifica se telegram_id do tipo int é convertido para str."""

        user = self._make_user(telegram_id=123)
        self.assertEqual(user.telegram_id, "123")

    def test_telegram_id_str_kept(self):
        """Verifica se telegram_id do tipo str é mantido sem alterações."""

        user = self._make_user(telegram_id="456")
        self.assertEqual(user.telegram_id, "456")

    def test_telegram_id_empty_raises_value_error(self):
        """Verifica se telegram_id vazio levanta ValueError."""

        with self.assertRaises(ValueError):
            self._make_user(telegram_id="")

    def test_telegram_id_zero_raises_value_error(self):
        """Verifica se telegram_id igual a zero levanta ValueError."""

        with self.assertRaises(ValueError):
            self._make_user(telegram_id=0)

    def test_telegram_id_invalid_type_raises_type_error(self):
        """Verifica se telegram_id de tipo inválido levanta TypeError."""

        with self.assertRaises(TypeError):
            self._make_user(telegram_id=["123"])

    def test_name_converts_to_str(self):
        """Verifica se name de tipo não-str é convertido para str."""

        user = self._make_user(name=42)
        self.assertEqual(user.name, "42")

    def test_name_none_kept(self):
        """Verifica se name igual a None é mantido sem alterações."""

        user = self._make_user(name=None)
        self.assertIsNone(user.name)

    def test_eq_with_user(self):
        """Verifica se dois Users com mesmo telegram_id são considerados
        iguais."""

        u1 = self._make_user(telegram_id="123")
        u2 = self._make_user(telegram_id="123")
        self.assertEqual(u1, u2)

    def test_eq_with_str(self):
        """Verifica se User é igual a uma str com o mesmo telegram_id."""

        user = self._make_user(telegram_id="123")
        self.assertEqual(user, "123")

    def test_eq_with_int(self):
        """Verifica se User é igual a um int com o mesmo telegram_id."""

        user = self._make_user(telegram_id="123")
        self.assertEqual(user, 123)

    def test_eq_different_ids(self):
        """Verifica se dois Users com telegram_ids diferentes são considerados
        diferentes."""

        u1 = self._make_user(telegram_id="123")
        u2 = self._make_user(telegram_id="456")
        self.assertNotEqual(u1, u2)

    def test_eq_unsupported_type_returns_false(self):
        """Verifica se a comparação com tipo não suportado retorna False."""

        user = self._make_user()
        self.assertFalse(user == 1.5)

    def test_telegram_text(self):
        """Verifica se telegram_text retorna o texto formatado corretamente."""

        user = self._make_user(telegram_id="123", name="Teste")
        expected = "Name: Teste\nTelegram ID: 123\n"
        self.assertEqual(user.telegram_text, expected)
