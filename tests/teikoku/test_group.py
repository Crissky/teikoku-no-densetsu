import unittest
from teikoku.register.group import Group


class TestGroup(unittest.TestCase):

    def _make_group(self, chat_id=-100123456789, name="Teste", silent=False):
        """Cria e retorna uma instância de Group com valores padrão."""

        return Group(chat_id=chat_id, name=name, silent=silent)

    def test_chat_id_valid(self):
        """Verifica se chat_id válido é aceito sem alterações."""

        group = self._make_group(chat_id=123456789)
        self.assertEqual(group.chat_id, 123456789)

    def test_chat_id_invalid_type_raises_type_error(self):
        """Verifica se chat_id de tipo inválido levanta TypeError."""

        with self.assertRaises(TypeError):
            self._make_group(chat_id="123")

    def test_name_valid(self):
        """Verifica se name válido é aceito sem alterações."""

        group = self._make_group(name="Meu Grupo")
        self.assertEqual(group.name, "Meu Grupo")

    def test_name_invalid_type_raises_type_error(self):
        """Verifica se name de tipo inválido levanta TypeError."""

        with self.assertRaises(TypeError):
            self._make_group(name=123)

    def test_silent_default_false(self):
        """Verifica se silent tem valor padrão False."""

        group = self._make_group()
        self.assertFalse(group.silent)

    def test_silent_true(self):
        """Verifica se silent=True é aceito."""

        group = self._make_group(silent=True)
        self.assertTrue(group.silent)

    def test_silent_invalid_type_raises_type_error(self):
        """Verifica se silent de tipo inválido levanta TypeError."""

        with self.assertRaises(TypeError):
            self._make_group(silent="true")

    def test_eq_with_group(self):
        """Verifica se dois Groups com mesmo chat_id são considerados
        iguais."""

        g1 = self._make_group(chat_id=123)
        g2 = self._make_group(chat_id=123)
        self.assertEqual(g1, g2)

    def test_eq_with_int(self):
        """Verifica se Group é igual a um int com o mesmo chat_id."""

        group = self._make_group(chat_id=123)
        self.assertEqual(group, 123)

    def test_eq_with_numeric_str(self):
        """Verifica se Group é igual a uma str numérica com o mesmo chat_id."""

        group = self._make_group(chat_id=123)
        self.assertEqual(group, "123")

    def test_eq_different_ids(self):
        """Verifica se dois Groups com chat_ids diferentes são considerados

        diferentes."""
        g1 = self._make_group(chat_id=123)
        g2 = self._make_group(chat_id=456)
        self.assertNotEqual(g1, g2)

    def test_eq_unsupported_type_returns_false(self):
        """Verifica se a comparação com tipo não suportado retorna False."""

        group = self._make_group()
        self.assertFalse(group == 1.5)

    def test_telegram_text(self):
        """Verifica se telegram_text é formatado corretamente."""

        group = self._make_group(chat_id=123, name="Teste")
        expected = (
            "Grupo: Teste\nID do Grupo: 123\nModo Silencioso: Não\n"
        )
        self.assertEqual(group.telegram_text, expected)

    def test_telegram_text_silent_true(self):
        """Verifica se telegram_text exibe 'Sim' quando silent=True."""

        group = self._make_group(chat_id=123, name="Teste", silent=True)
        expected = (
            "Grupo: Teste\nID do Grupo: 123\nModo Silencioso: Sim\n"
        )
        self.assertEqual(group.telegram_text, expected)
