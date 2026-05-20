import unittest
from datetime import datetime

from bson import ObjectId

from teikoku.entity.register.group import Group


class TestGroup(unittest.TestCase):

    def _make_group(
        self, chat_id=-100123456789, name="Teste", silent=False, **kwargs
    ):
        """Cria e retorna uma instância de Group com valores padrão."""

        return Group(chat_id=chat_id, name=name, silent=silent, **kwargs)

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
            "*Grupo*: Teste\n*ID do Grupo*: 123\n*Modo Silencioso*: Não\n"
        )
        self.assertEqual(group.telegram_text, expected)

    def test_telegram_text_silent_true(self):
        """Verifica se telegram_text exibe 'Sim' quando silent=True."""

        group = self._make_group(chat_id=123, name="Teste", silent=True)
        expected = (
            "*Grupo*: Teste\n*ID do Grupo*: 123\n*Modo Silencioso*: Sim\n"
        )
        self.assertEqual(group.telegram_text, expected)

    def test_updatable_attr_list(self):
        """Verifica se UPDATABLE_ATTR_LIST contém apenas 'silent'."""

        self.assertEqual(Group.UPDATABLE_ATTR_LIST, ("silent",))

    def test_has_updatable_attr_true(self):
        """Verifica se has_updatable_attr retorna True para 'silent'."""

        group = self._make_group()
        self.assertTrue(group.has_updatable_attr("silent"))

    def test_has_updatable_attr_false(self):
        """Verifica se has_updatable_attr retorna False para atributo não
        atualizável.
        """

        group = self._make_group()
        self.assertFalse(group.has_updatable_attr("name"))

    def test_id_default_is_object_id(self):
        """Verifica se _id padrão é um ObjectId."""

        group = self._make_group()
        self.assertIsInstance(group._id, ObjectId)

    def test_id_from_string(self):
        """Verifica se _id pode ser criado a partir de uma string válida."""

        oid = ObjectId()
        group = self._make_group(_id=str(oid))
        self.assertEqual(group._id, oid)

    def test_id_invalid_type_raises_type_error(self):
        """Verifica se _id de tipo inválido levanta TypeError."""

        with self.assertRaises(TypeError):
            self._make_group(_id=123)

    def test_created_at_none_by_default(self):
        """Verifica se created_at é None por padrão."""

        group = self._make_group()
        self.assertIsNone(group.created_at)

    def test_created_at_valid_datetime(self):
        """Verifica se created_at aceita um datetime válido."""

        now = datetime.now()
        group = self._make_group(created_at=now)
        self.assertEqual(group.created_at, now)

    def test_created_at_invalid_type_raises_type_error(self):
        """Verifica se created_at de tipo inválido levanta TypeError."""

        with self.assertRaises(TypeError):
            self._make_group(created_at="2024-01-01")

    def test_updated_at_none_by_default(self):
        """Verifica se updated_at é None por padrão."""

        group = self._make_group()
        self.assertIsNone(group.updated_at)

    def test_updated_at_valid_datetime(self):
        """Verifica se updated_at aceita um datetime válido."""

        now = datetime.now()
        group = self._make_group(updated_at=now)
        self.assertEqual(group.updated_at, now)

    def test_updated_at_invalid_type_raises_type_error(self):
        """Verifica se updated_at de tipo inválido levanta TypeError."""

        with self.assertRaises(TypeError):
            self._make_group(updated_at="2024-01-01")

    def test_to_dict_keys(self):
        """Verifica se to_dict retorna as chaves esperadas."""

        group = self._make_group(chat_id=123, name="Teste")
        result = group.to_dict()
        self.assertSetEqual(
            set(result.keys()),
            {"_id", "chat_id", "name", "silent", "created_at", "updated_at"},
        )

    def test_to_dict_values(self):
        """Verifica se to_dict retorna os valores corretos."""

        oid = ObjectId()
        group = self._make_group(chat_id=123, name="Teste", _id=oid)
        result = group.to_dict()
        self.assertEqual(result["chat_id"], 123)
        self.assertEqual(result["name"], "Teste")
        self.assertFalse(result["silent"])
