import logging

from repository.mongo.models.user import UserModel
from teikoku.user import User


logger = logging.getLogger(__name__)


def save_user(user: User) -> User:
    if not isinstance(user, User):
        raise TypeError(f"User precisa ser do tipo User ({type(user)}).")

    User_model = UserModel()
    User_model.save(user)
    saved_user = get_user_by_id(user.user_id)
    logger.info(
        f"User '{saved_user.name}' salvo com "
        f"USER ID '{saved_user.telegram_id}'"
    )

    return saved_user


def get_user_by_id(telegram_id: str) -> User:
    if not isinstance(telegram_id, str):
        raise TypeError("user_id precisa ser uma string.")

    user_model = UserModel()
    user = user_model.get(query={"user_id": telegram_id})

    return user


def exists_user(user_id: str) -> bool:
    if not isinstance(user_id, str):
        raise TypeError("user_id precisa ser uma string.")
    user_model = UserModel()

    return user_model.exists(_id=user_id)
