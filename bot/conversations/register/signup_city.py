from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, PrefixHandler

from bot.constants.command import SIGNUP_CITY_COMMANDS
from bot.constants.filter import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.decorators.group import only_group
from bot.decorators.player import need_signedup_player


@only_group
@need_signedup_player
async def signup_city(update: Update, context: ContextTypes.DEFAULT_TYPE): ...


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
