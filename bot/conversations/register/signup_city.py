from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, PrefixHandler

from bot.constants.command import SIGNUP_CITY_COMMANDS
from bot.constants.filter import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.decorators.group import only_group
from bot.decorators.player import need_signedup_player
from repository.mongo.functions.player import get_player_by_user_id
from repository.mongo.functions.world import get_world_by_chat_id
from teikoku.entity.city.city_base import City


@only_group
@need_signedup_player
async def signup_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cadastra Cidade do jogador"""

    chat_id = update._effective_chat.id
    user_id = update._effective_user.id
    player = get_player_by_user_id(user_id=user_id)
    world = get_world_by_chat_id(chat_id=chat_id)
    args = context.args
    city_name = args[0] if args else player.name
    city = City(
        name=city_name,
        chat_id=chat_id,
        owner=player,
    )


SIGNUP_CITY_HANDLERS = [
    # SIGNUP_CITY
    PrefixHandler(
        PREFIX_COMMANDS,
        SIGNUP_CITY_COMMANDS,
        signup_city,
        BASIC_COMMAND_FILTER,
    ),
    CommandHandler(SIGNUP_CITY_COMMANDS, signup_city, BASIC_COMMAND_FILTER),
]
