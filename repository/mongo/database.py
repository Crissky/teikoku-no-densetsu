import logging

from typing import Any, Union

from pymongo import MongoClient
from pymongo.cursor import Cursor
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult
from pymongo.synchronous.collection import Collection
from pymongo.synchronous.database import Database as MongoDatabase
from decouple import config

URL_CONNECTION = config("URL_CONNECTION")
DATABASE_NAME = config("DATABASE_NAME")
logger = logging.getLogger(__name__)


class Database:
    _instance = None

    def __init__(self, url_connection: str, database_name: str) -> None:
        self.__client = MongoClient(
            url_connection, serverSelectionTimeoutMS=5000
        )
        self.__server_info = self.__client.server_info()
        self.__database: MongoDatabase = self.__client[database_name]

    def get_collection(self, collection) -> Collection:
        return self.database[collection]

    def insert(self, collection: str, data: dict) -> InsertOneResult:
        col = self.get_collection(collection)

        return col.insert_one(document=data)

    def find(
        self, collection: str, query: dict, fields: Union[list, dict] = None
    ) -> Union[dict, None]:
        col = self.get_collection(collection)

        return col.find_one(filter=query, projection=fields)

    def find_many(
        self, collection: str, query: dict, fields: Union[list, dict] = None
    ) -> Cursor:
        col = self.get_collection(collection)

        return col.find(filter=query, projection=fields)

    def update(self, collection: str, query: dict, data: dict) -> UpdateResult:
        col = self.get_collection(collection)

        return col.update_one(filter=query, update=data)

    def replace(
        self, collection: str, query: dict, data: dict, upsert: bool = True
    ) -> UpdateResult:
        col = self.get_collection(collection)

        return col.replace_one(filter=query, replacement=data, upsert=upsert)

    def delete(self, collection: str, query: dict) -> DeleteResult:
        col = self.get_collection(collection)

        return col.delete_one(filter=query)

    def count(self, collection: str, query: dict, **kwargs: Any) -> int:
        col = self.get_collection(collection)

        return col.count_documents(filter=query, **kwargs)

    def length(self, collection: str, query: dict, field: str) -> int:
        col = self.get_collection(collection)
        cursor = col.aggregate(
            [
                {"$match": query},
                {"$project": {"length": {"$size": f"${field}"}}},
            ]
        )
        result = next(cursor, None)
        if result:
            return result["length"]

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Database(URL_CONNECTION, DATABASE_NAME)
        return cls._instance

    database = db = property(lambda self: self.__database)
    server_info = property(lambda self: self.__server_info)


if __name__ == "__main__":
    print(Database.get_instance())
