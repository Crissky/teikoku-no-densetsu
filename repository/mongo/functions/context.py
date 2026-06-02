from typing import Any, Optional

from telegram.ext import ContextTypes

from bot.enums.context import ContextDataTypeEnum, ContextKeyEnum


def put_obj(
    context: ContextTypes.DEFAULT_TYPE,
    key: ContextKeyEnum,
    obj: Any,
    user_id: Optional[int] = None,
):
    obj_dict = context.bot_data.get(key.name, {})
    if not obj_dict:
        context.bot_data[key.name] = obj_dict

    if not isinstance(user_id, int):
        user_id = obj.user_id

    obj_dict[user_id] = obj


def get_obj(
    context: ContextTypes.DEFAULT_TYPE,
    key: ContextKeyEnum,
    user_id: int,
) -> Any:
    return context.bot_data.get(key.name, {}).get(user_id)
