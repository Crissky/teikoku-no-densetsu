import logging

from repository.mongo.collection_enum import CollectionEnum
from repository.mongo.models.model import Model
from teikoku.user import User

logger = logging.getLogger(__name__)


class UserModel(Model):
    _class = property(lambda self: User)
    collection = property(lambda self: CollectionEnum.USER.value)


if __name__ == "__main__":
    print(" START LOCAL TEST ".center(79, "="))
    user = User(telegram_id=123456789, name="Teste")
    user_model = UserModel()

    print("COLLECTION NAME:")
    print(user_model.collection)

    print("\nSAVING USER...")
    user_model.save(user)
    saved_user = user_model.get(query={"telegram_id": "123456789"})

    print("\nGETTING SAVED USER...")
    print("\nSAVED USER:")
    print(saved_user)
    print("\nEQUALS:", user == saved_user)

    print(" END LOCAL TEST ".center(79, "="))
