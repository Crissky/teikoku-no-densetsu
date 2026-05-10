import logging
from decouple import config

from bot import CLOSE_MSG_HANDLER
from bot import SIGNUP_HANDLERS

from telegram.ext import Application

TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")
IS_PRODUCTION = config("IS_PRODUCTION", cast=bool, default=True)


# SET LOGGING ================================================================
logger = logging.getLogger(__name__)
if IS_PRODUCTION:
    logger.setLevel(logging.INFO)
else:
    logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("teikoku.log", mode="w")
console_handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
file_handler.stream.reconfigure(encoding='utf-8')
logger.addHandler(file_handler)
logger.addHandler(console_handler)
# SET LOGGING ================================================================


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add Single Handler =====================================================
    application.add_handler(CLOSE_MSG_HANDLER)

    # Add Multiple Handlers ==================================================
    application.add_handlers(SIGNUP_HANDLERS)


    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
