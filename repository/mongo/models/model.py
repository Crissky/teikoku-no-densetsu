import logging

from abc import ABC, abstractmethod
from typing import Union, Any, List

from bson import ObjectId

from general.functions.date_time import get_brazil_time_now
from repository.mongo.database import Database

from teikoku.register.group import Group  # noqa
from teikoku.register.player import Player  # noqa

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
            populate_result = self.__populate_load(result)
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
                self.instanciate_class(self.__populate_load(item))
                for item in result
            ]
        elif len(fields) == 1:
            result = [item[fields[0]] for item in result]
        else:
            result = list(result)

        return result

    def save(self, obj: Any, replace=False):
        if not isinstance(obj, self._class):
            raise ValueError(
                f"Objeto inválido. Precisa ser {self._class} não {type(obj)}"
            )

        obj_dict = obj.to_dict()
        obj_dict["_class"] = obj.__class__.__name__
        query = {}
        if isinstance(obj._id, ObjectId):
            query["_id"] = obj._id
        else:
            obj_dict.pop("_id", None)
            if obj_dict.get(self.alternative_id, None):
                query[self.alternative_id] = obj_dict[self.alternative_id]

        if query and self.database.find(self.collection, query):
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

    def __populate_load(self, dict_obj: dict):
        """Função que popula os campos do objeto que são outras classes e que
        no banco são salvos somente a sua chave. Esses campo que serão
        populados pertencem a outra tabela e por conta disso
        devem possuir sua própria classe Model.

        Quando o campo a ser populado é uma lista, todos os elementos da lista
        serão populados, porém todos eles devem pertencer a mesma tabela."""
        for popu_field_name, popu_field_info in self.populate_fields.items():
            expected_class = popu_field_info.get("_class")
            is_same_class = (
                issubclass(eval(dict_obj["_class"]), eval(expected_class))
                if expected_class
                else False
            )
            if expected_class and not is_same_class:
                continue

            if popu_field_info["id_key"] in dict_obj.keys():
                mongo_field_name = popu_field_info["id_key"]
                popu_field_args = dict_obj.pop(mongo_field_name)
                model = popu_field_info.get("model")

                _object = None
                if isinstance(popu_field_args, list):
                    _object = []
                    for item in popu_field_args:
                        if isinstance(item, dict):
                            item_id = item.pop("_id", None)
                            if "subclass" in popu_field_info.keys():
                                item_loaded = model.get(item_id)
                                subclass = popu_field_info["subclass"]
                                item_loaded = subclass(item_loaded, **item)
                            # Instancia a classe novamente combinando os
                            # atributos fixo do objeto (que vem com model)
                            # com os atributos variáveis
                            # (que estão na lista do mongo).
                            elif "remakeclass" in popu_field_info.keys():
                                item_loaded = model.get(item_id)
                                remakeclass = item_loaded.__class__
                                item_loaded_dict = item_loaded.to_dict()
                                item_loaded_dict.update(item)
                                item_loaded = remakeclass(**item_loaded_dict)
                            elif "factory" in popu_field_info.keys():
                                factory = popu_field_info["factory"]
                                item_loaded = factory(**item)
                            _object.append(item_loaded)
                        elif isinstance(item, (ObjectId, str)):
                            _object.append(model.get(item))
                        else:
                            raise KeyError(
                                f'O valor da id_key "{mongo_field_name}" '
                                'no "dict_obj" é uma lista e um elemento '
                                "dessa lista não é um dict com o "
                                f'campo "_id", str ou ObjectId. item: {item}.'
                            )
                # esperado que dict_field seja um _id
                elif popu_field_args is not None:
                    if "factory" in popu_field_info.keys():
                        factory = popu_field_info["factory"]
                        _object = factory(popu_field_args)
                    else:
                        _object = model.get(popu_field_args)

                dict_obj[popu_field_name] = _object
            else:
                if isinstance(self._class, tuple):
                    class_name = ", ".join([c.__name__ for c in self._class])
                else:
                    class_name = self._class.__name__
                raise KeyError(
                    f"O dicionário da(s) classe(s) {class_name} "
                    f'não possui campo {popu_field_info["id_key"]}.'
                )

        return dict_obj

    def instanciate_class(self, populate_result: dict):
        _class = eval(populate_result.pop("_class"))
        return _class(**populate_result)

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
    def populate_fields(self) -> dict:
        """
        Retorna um dicionário com os campos necessários para criar
        os objetos de outros modelos necessários para o modelo atual.

        field_name: Nome do campo que será populado ao criar o objeto.
        id_key: caminho do campo usando para buscar o objeto no banco
            (aka _id ou alternative_id).
        model: Modelo usado para carregar o objeto que populará
            o objeto do modelo atual.
        subclass: Class que será usada para instanciar novos objetos.
            Essa classe usará o objeto carregado pelo `model` como um
            dos seus atributos, além dos demais chaves/valores do
            dicionário salvo no banco.
            Usado quando o campo é salvo no banco do objeto pai como
            uma lista de dicionários (Usado no BagModel para usar os
            objetos do tipo Equipment/Consumable carregados pelo
            ItemModel como atributo da classe Item).
        remakeclass: Se existir esse campo, define que a Classe que
            será instanciada usando o to_dict() do
            objeto carregado do banco pelo `model` como seus
            atributos, além dos demais chaves/valores do dicionário
            salvo no banco. (Usado pelo StatusModel para modificar
            valores que deveriam ser variáveis [como turno e level] da
            classe Condition sem alterar os valores padrão [como nome
            e descrição]).
        factory: Função que ira carregar o atributo a partir de uma
            função factory usando como argumentos os campos vindos do
            Mongo, ao invés de carregar do banco a partir de um Model.
        _class: Atributo só será populado em objetos que
            são dessa classe. (Usando em ItemModel para popular
            atributo somente da classe Consumable e não tenta na
            Classe Equipment, pois levantaria um erro).

        populate_fields = {
            'field_name': {
                'id_key': string,
                'model': Model,
                'subclass': Any Class,
            },
            ...
        }
        Exemplo:
        populate_fields = {
            'race': {
                'id_key': 'race_name',
                'model': RaceModel,
            }
        }
        Exemplo2:
        populate_fields = {
            'items': {
                'id_key': 'items_ids',
                'model': ItemModel(),  # Carrega equipamentos e consumíveis
                'subclass': Item  # Usa o equipamento/consumível carregado
                    como atributo ao instanciar a classe Item
            }
        }
        Exemplo3:
        populate_fields = {
            'conditions': {
                'id_key': 'condition_args',
                'model': ConditionModel(),
                'remakeclass': True,  # Se a Classe será reinstanciada
            }
        }
        Exemplo4:
        'condition': {
            'id_key': 'condition_name',
            '_class': 'Consumable',  # Atributo 'condition'
                só será populado em objetos dessa classe.
            'model': ConditionModel()
        }
        Exemplo4:
        'condition': {
            'id_key': 'condition_name',
            'factory': factory_condition # Função Factory
        },
        """
        return {}
