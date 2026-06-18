from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, PrefixHandler

from bot.constants.command import WORLD_COMMANDS
from bot.constants.filter import BASIC_COMMAND_FILTER, PREFIX_COMMANDS
from bot.decorators.player import need_signedup_player


@need_signedup_player
async def show_world(update: Update, context: ContextTypes.DEFAULT_TYPE): ...


WORLD_HANDLERS = [
    # SHOW
    PrefixHandler(
        PREFIX_COMMANDS, WORLD_COMMANDS, show_world, BASIC_COMMAND_FILTER
    ),
    CommandHandler(WORLD_COMMANDS, show_world, BASIC_COMMAND_FILTER),
]
