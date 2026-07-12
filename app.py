import logging
from decouple import config

from bot import (
    CLOSE_MSG_HANDLER,
    SET_GROUP_HANDLERS,
    SET_PLAYER_HANDLERS,
    SIGNUP_GROUP_HANDLERS,
    SIGNUP_PLAYER_HANDLERS,
    SIGNUP_WORLD_HANDLERS,
    SHOW_GROUP_HANDLERS,
    SHOW_PLAYER_HANDLERS,
    SHOW_WORLD_HANDLERS,
    WORLD_HANDLERS,
)

from telegram.ext import Application

TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")
IS_PRODUCTION = config("IS_PRODUCTION", cast=bool, default=True)


# SET LOGGING ================================================================
if IS_PRODUCTION:
    level = logging.INFO
else:
    level = logging.DEBUG

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

file_handler = logging.FileHandler("teikoku.log", mode="w", encoding="utf-8")
console_handler = logging.StreamHandler()
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

root_logger = logging.getLogger()
root_logger.setLevel(level)

root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)
# SET LOGGING ================================================================

logger = logging.getLogger(__name__)


def main() -> None:
    """Run the bot."""

    logger.info("Iniciando Teikoku no Densetshu...")
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    logger.info("Adicionando handlers.")
    # Add Single Handler =====================================================
    application.add_handler(CLOSE_MSG_HANDLER)

    # Add Multiple Handlers ==================================================
    application.add_handlers(SET_GROUP_HANDLERS)
    application.add_handlers(SET_PLAYER_HANDLERS)
    application.add_handlers(SIGNUP_PLAYER_HANDLERS)
    application.add_handlers(SIGNUP_GROUP_HANDLERS)
    application.add_handlers(SIGNUP_WORLD_HANDLERS)
    application.add_handlers(SHOW_GROUP_HANDLERS)
    application.add_handlers(SHOW_PLAYER_HANDLERS)
    application.add_handlers(SHOW_WORLD_HANDLERS)
    application.add_handlers(WORLD_HANDLERS)

    logger.info("Iniciando run_polling() Teikoku no Densetshu!")
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
