import logging

from typing import Any, Iterable, Optional, Tuple, Type, get_type_hints

from telegram import Update
from telegram.ext import CallbackContext

from repository.mongo.base import MongoBase
from repository.mongo.enums.field import (
    AltIdEnum,
    ContextAltIdEnum,
    UpdateAltIdEnum,
)
from repository.mongo.models.model import Model

logger = logging.getLogger(__name__)


def save_entity(
    entity: MongoBase,
    entity_type: Type[MongoBase],
    model_type: Type[Model],
    key_value_type: Type[Any],
    key_field_enum: AltIdEnum,
) -> MongoBase:
    if not isinstance(entity, entity_type):
        raise TypeError(
            f"entity precisa ser do tipo {entity_type} ({type(entity)})."
        )

    model = model_type()
    model.save(entity)
    key_field = key_field_enum.value
    key_value = getattr(entity, key_field)
    retrieved_entity = get_entity_by_alt_id(
        model_type=model_type,
        key_value=key_value,
        key_value_type=key_value_type,
        key_field_enum=key_field_enum,
    )
    logger.info(
        f"{entity_type.__name__} salvo com " f"{key_field}='{key_value}'"
    )

    return retrieved_entity


def update_entity(
    args: Iterable[Tuple[str, Any]],
    entity_type: Type[MongoBase],
    model_type: Type[Model],
    key_value_type: Type[Any],
    key_field_enum: AltIdEnum,
    update_key_field_enum: UpdateAltIdEnum,
    entity: Optional[MongoBase] = None,
    update: Optional[Update] = None,
) -> Optional[MongoBase]:
    if isinstance(update, Update) and entity is None:
        entity = get_entity(
            model_type=model_type,
            key_value_type=key_value_type,
            key_field_enum=key_field_enum,
            update_key_field_enum=update_key_field_enum,
            context_key_field_enum=None,
            update=update,
            context=None,
        )

    if not isinstance(entity, entity_type):
        raise TypeError(
            f"entity precisa ser do tipo {entity_type} ({type(entity)})."
        )

    is_updated = False
    retrieved_entity = None
    group_type_hints = get_type_hints(entity)
    for attr, value in args:
        if entity.has_updatable_attr(attr):
            group_attr_type = group_type_hints[attr]
            if group_attr_type == type(value):
                setattr(entity, attr, value)
                is_updated = True
            else:
                logger.warning(
                    f"O atributo '{attr}' não pode ser atualizado com o valor "
                    f"do tipo {type(value)}, pois o tipo esperado é "
                    f"{type(group_attr_type)}."
                )
        else:
            logger.warning(
                f"Group não possui ou não pode alterar o atributo '{attr}'."
            )

    if is_updated:
        model = model_type()
        model.save(entity)
        key_field = key_field_enum.value
        key_value = getattr(entity, key_field)
        retrieved_entity = get_entity_by_alt_id(
            model_type=model_type,
            key_value=key_value,
            key_value_type=key_value_type,
            key_field_enum=key_field_enum,
        )

        return retrieved_entity


def get_entity_by_alt_id(
    model_type: Type[Model],
    key_value: Any,
    key_value_type: Type[Any],
    key_field_enum: AltIdEnum,
) -> MongoBase:
    if not isinstance(key_value, key_value_type):
        raise TypeError(
            f"key_value precisa ser um {key_value_type} ({type(key_value)})."
        )

    model = model_type()
    key_field = key_field_enum.value
    query = {key_field: key_value}
    entity = model.get(query=query)

    return entity


def get_entity(
    model_type: Type[Model],
    key_value_type: Type[Any],
    key_field_enum: AltIdEnum,
    update_key_field_enum: UpdateAltIdEnum,
    context_key_field_enum: ContextAltIdEnum,
    update: Optional[Update] = None,
    context: Optional[CallbackContext] = None,
) -> MongoBase:
    if isinstance(update, Update):
        update_key_field = update_key_field_enum.value
        key_value = getattr(update, update_key_field).id
    elif isinstance(context, CallbackContext):
        context_key_field = context_key_field_enum.value
        key_value = getattr(context, context_key_field)
    else:
        raise ValueError("É preciso informar ou update ou context.")

    return get_entity_by_alt_id(
        model_type=model_type,
        key_value=key_value,
        key_value_type=key_value_type,
        key_field_enum=key_field_enum,
    )


def exists_entity(
    model_type: Type[Model],
    update_key_field_enum: UpdateAltIdEnum,
    context_key_field_enum: ContextAltIdEnum,
    key_value: Any = None,
    update: Optional[Update] = None,
    context: Optional[CallbackContext] = None,
) -> bool:
    if isinstance(update, Update):
        update_key_field = update_key_field_enum.value
        key_value = getattr(update, update_key_field).id
    elif isinstance(context, CallbackContext):
        context_key_field = context_key_field_enum.value
        key_value = getattr(context, context_key_field)
    else:
        raise ValueError("É preciso informar ou update ou context.")

    model = model_type()

    return model.exists(_id=key_value)
