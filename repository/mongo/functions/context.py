from typing import Any, Optional

from telegram.ext import ContextTypes

from bot.enums.context import ContextDataTypeEnum, ContextKeyEnum


def put_obj(
    context: ContextTypes.DEFAULT_TYPE,
    key: ContextKeyEnum,
    obj: Any,
    telegram_id: int,
    data_type: ContextDataTypeEnum = ContextDataTypeEnum.BOT,
):
    if data_type == ContextDataTypeEnum.BOT:
        data = context.bot_data
    elif data_type == ContextDataTypeEnum.CHAT:
        data = context.chat_data
    elif data_type == ContextDataTypeEnum.USER:
        data = context.user_data

    data_dict = data.setdefault(key.name, {})
    data_dict[telegram_id] = obj


def get_obj(
    context: ContextTypes.DEFAULT_TYPE,
    key: ContextKeyEnum,
    telegram_id: int,
    data_type: ContextDataTypeEnum = ContextDataTypeEnum.BOT,
) -> Any:
    if data_type == ContextDataTypeEnum.BOT:
        data = context.bot_data
    elif data_type == ContextDataTypeEnum.CHAT:
        data = context.chat_data
    elif data_type == ContextDataTypeEnum.USER:
        data = context.user_data

    return data.get(key.name, {}).get(telegram_id)


def put_user_obj(
    context: ContextTypes.DEFAULT_TYPE,
    key: ContextKeyEnum,
    obj: Any,
    user_id: Optional[int] = None,
    data_type: ContextDataTypeEnum = ContextDataTypeEnum.USER,
):

    if not isinstance(user_id, int):
        user_id = obj.user_id

    return put_obj(
        context=context, key=key, telegram_id=user_id, data_type=data_type
    )


def get_user_obj(
    context: ContextTypes.DEFAULT_TYPE,
    key: ContextKeyEnum,
    user_id: int,
    data_type: ContextDataTypeEnum = ContextDataTypeEnum.USER,
) -> Any:
    return get_obj(
        context=context,
        key=key,
        telegram_id=user_id,
        data_type=data_type,
    )

