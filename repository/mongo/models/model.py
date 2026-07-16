import logging

from abc import ABC, abstractmethod
from typing import Dict, Union, Any, List

from bson import ObjectId

from general.functions.date_time import get_brazil_time_now
from repository.mongo.database import Database
from repository.mongo.enums.field import PopulateFieldEnum

# from teikoku.entity.register.group import Group  # noqa
# from teikoku.entity.register.player import Player  # noqa
# from teikoku.entity.world.world import World  # noqa

logger = logging.getLogger(__name__)


class Model(ABC):
    """Classe Base usada para salvar Classes no Banco de Dados MongoDB"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __alt_id_is_valid(self):
        return isinstance(self.alternative_id, str)

    def _extract_attributes(self, data: dict, definition: dict) -> dict:
        new_data = {}
        for attribute_name in definition["attributes"]:
            new_data[attribute_name] = data[attribute_name]

        return new_data

    def _object_to_dict(self, obj: Any) -> dict:
        obj_dict: dict = obj.to_dict()
        for field_name, definition in self.save_fields:
            new_data = {}
            field_data = obj_dict[field_name]
            if isinstance(field_data, list):
                new_data[field_name] = [
                    self._extract_attributes(data, definition)
                    for data in field_data
                ]
            else:
                new_data[field_name] = self._extract_attributes(
                    field_data, definition
                )
            obj_dict.update(new_data)

        return obj_dict

    def get_query_by_id(self, _id: Union[int, ObjectId, str]):
        query = None
        if isinstance(_id, ObjectId):
            query = {"_id": _id}
        elif ObjectId.is_valid(_id):
            query = {"_id": ObjectId(_id)}
        elif isinstance(_id, (int, str)) and self.__alt_id_is_valid():
            query = {self.alternative_id: _id}
        else:
            raise ValueError(
                "ID inválido. O ID Precisa ser um inteiro ou ObjectId ou "
                "uma string com 24 caracteres que representa um ObjectId."
                f"ID: {_id}, Tipo: {type(_id)}"
            )
        return query

    def check_query(self, query: dict):
        if not query:
            raise ValueError("Query esta vazia.")
        if not isinstance(query, dict):
            raise ValueError("Query precisa ser um dicionário.")

    def delete(
        self, _id: Union[int, ObjectId, str] = None, query: dict = None
    ) -> Any:
        if _id:
            query = self.get_query_by_id(_id)
        self.check_query(query)
        return self.database.delete(self.collection, query)

    def get(
        self,
        _id: Union[int, ObjectId, str] = None,
        query: dict = None,
        fields: Union[dict, list, str] = None,
        partial: bool = True,
    ) -> Union[Any, dict]:
        """Retorna um objeto instanciado com os dados oriundos do
        Banco de Dados.

        Se fields for passado e partial for True,
        retorna apenas os campos desejados em formato dict.

        Se fields for passado e partial não for True,
        retorna o objeto instanciado com os campos desejados passados como
        argumentos e os demais usarão o default da classe.
        """

        if _id:
            query = self.get_query_by_id(_id)
        self.check_query(query)
        if isinstance(fields, str):
            fields = [fields]
        if result := self.database.find(self.collection, query, fields):
            if fields and partial is True:
                return result
            populate_result = self._populate_load(result)
            return self.instanciate_class(populate_result)

    def get_all(
        self, query: dict = None, fields: Union[dict, list, str] = None
    ) -> List[Union[Any, dict]]:
        """Retorna uma lista de objetos instanciados com os dados
        oriundos do Banco de Dados.

        Se fields for passado com um único campo, retorna uma lista com os
        valores do campo passado

        Se fields for passado com vários campos, retorna uma lista de dict com
        os campos em fields.
        """

        if isinstance(fields, str):
            fields = [fields]

        result = self.database.find_many(self.collection, query, fields)

        if not fields:
            result = [
                self.instanciate_class(self._populate_load(item))
                for item in result
            ]
        elif len(fields) == 1:
            result = [item[fields[0]] for item in result]
        else:
            result = list(result)

        return result

    # TODO Usar o alternative_id como primeira alternativa da query
    def save(self, obj: Any, replace=False):
        if not isinstance(obj, self._class):
            raise ValueError(
                f"Objeto inválido. Precisa ser {self._class} não {type(obj)}"
            )

        obj_dict = self._object_to_dict(obj=obj)
        query = {}
        if obj_dict.get(self.alternative_id, None):
            obj_dict.pop("_id", None)
            query[self.alternative_id] = obj_dict[self.alternative_id]
        elif isinstance(obj._id, ObjectId):
            query["_id"] = obj._id
        else:
            raise KeyError(
                "Objeto precisa ter o campo '_id' ou "
                f"'{self.alternative_id}' preenchido."
            )

        if query and self.database.find(self.collection, query):
            obj_dict.pop("created_at", None)
            if not replace:
                logger.info(f"Updating: {self.__class__.__name__}")
                obj_dict["updated_at"] = get_brazil_time_now()
                result = self.database.update(
                    collection=self.collection,
                    query=query,
                    data={"$set": obj_dict},
                )
            elif replace:
                logger.info(f"Replacing: {self.__class__.__name__}")
                obj_dict["updated_at"] = get_brazil_time_now()
                result = self.database.replace(
                    collection=self.collection, query=query, data=obj_dict
                )
        else:
            logger.info(f"Inserting: {self.__class__.__name__}")
            obj_dict["created_at"] = get_brazil_time_now()
            obj_dict["updated_at"] = get_brazil_time_now()
            result = self.database.insert(self.collection, obj_dict)

        return result

    def exists(self, _id: Union[int, ObjectId, str]) -> bool:
        if _id:
            query = self.get_query_by_id(_id)
        self.check_query(query)

        return bool(self.database.count(self.collection, query, limit=1))

    def length(
        self,
        field: str,
        _id: Union[int, ObjectId, str] = None,
        query: dict = None,
    ) -> int:
        if _id:
            query = self.get_query_by_id(_id)
        self.check_query(query)
        return self.database.length(self.collection, query, field)

    # TODO Refatorar para não precisar mais salvar o _class no Banco
    def _populate_load(self, dict_obj: dict):
        """
        Popula campos do objeto que referenciam outras classes que podem estar
        armazenadas em coleções diferentes do banco de dados.

        Esta função é responsável por carregar e/ou instanciar objetos
        relacionados. Cada campo populado deve ter seu prório método
        instanciador (INITIATOR) e, opcionalmente, um método de
        callback (CALLBACK) que retorne o objeto instanciado como resultado.

        Pipeline:
          - Se o campo tiver definido o INITIATOR, todos os dados serão usados
            no INITIATOR. Mas, caso o campo também tenha definido o CALLBACK,
            o INITIATOR receberá somente um dicionário contendo o "_id" e o
            CALLBACK receberá o resultado do INITIATOR e os demais dados do
            campo.

        Comportamento:
          - Para campos simples: carrega e instancia o objeto referenciado
          - Para campos do tipo lista: carrega e instancia todos os elementos,
            passando seus dados pelo mesmo pipeline.

        Exemplo (somente INITIATOR)
            return INITIATOR(field)
        Exemplo (INITIATOR e CALLBACK)
            return CALLBACK(INITIATOR(field.pop("_id")), **field)

        Args:
            dict_obj (dict): Dicionário contendo os dados do objeto a ser
            populado.

        Returns:
            dict: Dicionário com os campos populados com objetos instanciados.
        """

        for p_field_name, p_definition in self.populate_fields.items():
            obj = dict_obj[p_field_name]
            if isinstance(obj, list):
                obj = [
                    self._populate_field(item, p_field_name, p_definition)
                    for item in obj
                ]
            else:
                obj = self._populate_field(obj, p_field_name, p_definition)

            dict_obj[p_field_name] = obj

        return dict_obj

    def _populate_field(self, obj: dict, field_name: str, definition: dict):
        """Carrega os dados de um campo."""

        initiator = definition.get(PopulateFieldEnum.INITIATOR)
        callback = definition.get(PopulateFieldEnum.CALLBACK)
        if not initiator:
            raise KeyError(
                "É obrigatório ter um campo "
                f"{PopulateFieldEnum.INITIATOR} no definition do campo "
                f"{field_name}."
            )

        if hasattr(initiator, "get"):
            initiator_call = initiator().get
        elif callable(initiator):
            initiator_call = initiator
        else:
            raise TypeError(
                f"initiator do campo {field_name} precisa ser um "
                "callable ou um objeto com o método get."
            )

        if callback:
            query = {"_id": obj.pop("_id")}
            callback_obj = initiator_call(query)
            obj = callback(callback_obj, **obj)
        else:
            obj = initiator_call(obj)

        return obj

    def instanciate_class(self, populate_result: dict):
        return self._class(**populate_result)

    database: Database = property(lambda self: Database.get_instance())

    @property
    @abstractmethod
    def alternative_id(self) -> str: ...

    @property
    @abstractmethod
    def collection(self) -> str: ...

    @property
    @abstractmethod
    def _class(self) -> Any: ...

    @property
    def save_fields(self) -> Dict[str, Dict[PopulateFieldEnum, Any]]:
        """
        Retorna um dicionário com os campos (e suas definições) que precisam
        de algum tratamento para serem salvos no banco de dados. Esse campo
        será salvo no banco como um object ou uma lista de objects.

        field_name: Nome do campo que precisa de tratamento especial
            para ser salvo.

            SaveFieldEnum.ATTRIBUTES: lista de strings com os nomes dos
            atributos do campo que serão salvos no banco.

        save_fields = {
            'cities': {
                SaveFieldEnum.ATTRIBUTES: ["_id"]
            }
            ...
        }
        """

        return {}

    @property
    def populate_fields(self) -> Dict[str, Dict[str, Any]]:
        """
        Retorna um dicionário com os campos necessários para criar
        os objetos de outros modelos usados pelo modelo atual.

        field_name: Nome do campo que será populado ao criar o objeto.

            PopulateFieldEnum.INITIATOR (Callable): Callable que usa os dados
            do campo para populá-lo com um novo objeto.

            PopulateFieldEnum.CALLBACK (Callable): Se CALLBACK for definido,
            somente o "_id" será usado no INITIATOR e o valor retornado
            juntamente com os demais dados do campo serão passados para o
            CALLBACK para criar o objeto final que populará o campo.

        populate_fields = {
            'field_name': {
                PopulateFieldEnum.INITIATOR: Model,
            },
            ...
        }

        Exemplo1:
        populate_fields = {
            'race': {
                PopulateFieldEnum.INITIATOR: RaceModel,
            }
        }

        Exemplo2:
        populate_fields = {
            'items': {
                # Carrega equipamentos e consumíveis
                PopulateFieldEnum.INITIATOR: ItemModel,
                # Usa o equipamento/consumível carregado como atributo
                # ao instanciar a classe Item
                PopulateFieldEnum.CALLBACK: Item
            }
        }

        """
        return {}
