from telegram import Update
from telegram.ext import ContextTypes


# TODO Criar need_signedup_world
def need_signedup_world(callback):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE): ...
