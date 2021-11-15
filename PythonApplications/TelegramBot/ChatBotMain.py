# pip install python-telegram-bot
from telegram import Update
from telegram.ext import *
import Responses

from Infrastructure.Logger_Infrastructure.Projects_Logger import BuildLogger, print_before_logger


PROJECT_NAME = 'Telegram Bot'
SITE = ''

API_KEY = '2142997401:AAELi6adP_gxfgcRarNtDsM1Maoi3uLs4AA'


def start_command(update: Update, context: CallbackContext) -> None:
    """Sends a start message."""

    update.message.reply_text(
        "Hello, this is Bot that can answer for sample and complex responses\n\n"
        "Use /help to get help from the bot\n"
        "Use /clear to clear the stored data so that you can see\n"
        "Use /examples to get sample and complex responses\n"
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """ Displays info on how to use the bot. """

    update.message.reply_text(
        "Use /start to test this bot.\n"
        "Use /clear to clear the stored data so that you can see\n"
        "Use /examples to get sample and complex responses\n"
    )


def clear_command(update: Update, context: CallbackContext) -> None:
    """ Clears the callback data cache """

    context.bot.callback_data_cache.clear_callback_data()  # type: ignore[attr-defined]
    context.bot.callback_data_cache.clear_callback_queries()  # type: ignore[attr-defined]
    update.effective_message.reply_text(
        "All clear!\n"
        "Use /start to test this bot.\n"
        "Use /examples to get sample and complex responses\n"
    )


def examples_command(update: Update, context: CallbackContext) -> None:
    """ Clears the callback data cache """

    update.message.reply_text(
        'For sample responses use can send "hi", "hello" or ask "who are you?".\n'
        'For complex responses use can ask "what is the time?" or send "I want stock data".\n'
    )


def handle_message(update: Update, context: CallbackContext) -> None:
    text = str(update.message.text).lower()
    flag_response = False

    response = Responses.sample_responses(text)
    if response:
        flag_response = True
        update.message.reply_text(response)

    response = Responses.complex_responses(text, update)
    if response:
        flag_response = True
        update.message.reply_text(response)

    if not flag_response:
        update.message.reply_text(
            "I don't understand you.\n\n"
            "Use /start to test this bot.\n"
            "Use /help to get help from the bot\n"
            "Use /clear to clear the stored data so that you can see\n"
            "Use /examples to get sample and complex responses\n"
        )


def error(update: Update, context: CallbackContext) -> None:
    logger.error(f'Update {update} caused error {context.error}')


def main():
    updater = Updater(API_KEY, use_context=True)

    updater.dispatcher.add_handler(CommandHandler("start", start_command))
    updater.dispatcher.add_handler(CommandHandler("help", help_command))
    updater.dispatcher.add_handler(CommandHandler('clear', clear_command))
    updater.dispatcher.add_handler(CommandHandler('examples', examples_command))

    updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

    updater.dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    print_before_logger(project_name=PROJECT_NAME, site=SITE)
    logger = BuildLogger(project_name=PROJECT_NAME, site=SITE).build_logger(debug=True)

    main()
