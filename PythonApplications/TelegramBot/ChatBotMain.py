# pip install python-telegram-bot
from telegram import Update, ParseMode
from telegram.ext import *
import Responses

from PrivateInfrastructure.Logger_Infrastructure.Projects_Logger import BuildLogger, print_before_logger
from PythonApplications.TelegramBot.TelegramBotUserDetails import TelegramBotUserDetails
from dataclasses import dataclass

PROJECT_NAME = 'Telegram Bot'
SITE = ''

API_KEY = '2142997401:AAELi6adP_gxfgcRarNtDsM1Maoi3uLs4AA'
USER_DETAILS = {}


@dataclass()
class ReturnFunctionDetailsString:
    start = "Use /start to test this bot."
    help = 'Use /help to get help from the bot.'
    clear = 'Use /clear to clear the stored data so that you can see.'
    examples = 'Use /examples to get sample and complex responses.'
    get_default_stacks = 'Use /get_default_stacks to get default stacks.'
    get_specific_stacks = 'Use /get_specific_stacks to get default stacks.'


def start_command(update: Update, context: CallbackContext) -> None:
    """Sends a start message."""

    update.message.reply_text(
        f"Hello, this is Bot that can answer for sample and complex responses\n\n"
        f"{ReturnFunctionDetailsString.help}\n"
        f"{ReturnFunctionDetailsString.clear}\n"
        f"{ReturnFunctionDetailsString.examples}\n\n"
        # f"{ReturnFunctionDetailsString.get_default_stacks}\n\n"
    )

    if not USER_DETAILS.get(update.effective_user.id):
        USER_DETAILS[update.effective_user.id] = TelegramBotUserDetails()
        update.message.reply_text("What is your first name?\n")


def help_command(update: Update, context: CallbackContext) -> None:
    """ Displays info on how to use the bot. """

    update.message.reply_text(
        f"{ReturnFunctionDetailsString.start}.\n"
        f"{ReturnFunctionDetailsString.clear}\n"
        f"{ReturnFunctionDetailsString.examples}\n"
        f"{ReturnFunctionDetailsString.get_default_stacks}\n"
        f"{ReturnFunctionDetailsString.get_specific_stacks}\n\n"
    )


def clear_command(update: Update, context: CallbackContext) -> None:
    """ Clears the callback data cache """
    del USER_DETAILS[update.effective_user.id]

    context.bot.callback_data_cache.clear_callback_data()  # type: ignore[attr-defined]
    context.bot.callback_data_cache.clear_callback_queries()  # type: ignore[attr-defined]
    update.effective_message.reply_text(
        "All clear!\n"
        f"{ReturnFunctionDetailsString.start}\n"
        f"{ReturnFunctionDetailsString.help}\n"
        f"{ReturnFunctionDetailsString.examples}\n"
    )


def examples_command(update: Update, context: CallbackContext) -> None:
    """ Clears the callback data cache """

    update.message.reply_text(
        'For sample responses use can send "hi", "hello" or ask "who are you?".\n'
        'For complex responses use can ask "what is the time?" or send "I want stock data".\n'
    )


def get_default_stacks(update: Update, context: CallbackContext) -> None:
    """ Clears the callback data cache """
    response = Responses.get_default_stacks_responses(user_details=USER_DETAILS[update.effective_user.id], update=update)
    update.message.bot.send_photo(chat_id=update.message.chat.id, photo=open(response, 'rb'))
    # update.message.bot.sendDocument(chat_id=update.message.chat.id, document=open(response, 'rb'))


def get_specific_stacks(update: Update, context: CallbackContext) -> None:
    """ Clears the callback data cache """
    update.message.reply_text(
        'What is your stacks?\n'
        'Please send "My stacks is: stack_1, stack_2\n'
    )


def handle_message(update: Update, context: CallbackContext) -> None:
    text = str(update.message.text).lower()

    if (
            (response := Responses.sample_user_details(USER_DETAILS[update.effective_user.id], text))
            or (response := Responses.sample_responses(text))
            or not (response := Responses.sample_responses(text))
            and (response := Responses.complex_responses_str(text, update))
    ):
        update.message.reply_text(response)
    elif response := Responses.complex_responses_img(text, update):
        update.message.bot.send_photo(chat_id=update.message.chat.id, photo=open(response, 'rb'))
        # update.message.bot.sendDocument(chat_id=update.message.chat.id, document=open(response, 'rb'))
    else:
        update.message.reply_text(
            "I don't understand you.\n\n"
            f"{ReturnFunctionDetailsString.start}\n"
            f"{ReturnFunctionDetailsString.help}\n"
            f"{ReturnFunctionDetailsString.clear}\n"
            f"{ReturnFunctionDetailsString.examples}\n"
        )


def error(update: Update, context: CallbackContext) -> None:
    logger.error(f'Update {update} caused error {context.error}')


def main():
    updater = Updater(API_KEY, use_context=True)

    updater.dispatcher.add_handler(CommandHandler("start", start_command))
    updater.dispatcher.add_handler(CommandHandler("help", help_command))
    updater.dispatcher.add_handler(CommandHandler('clear', clear_command))
    updater.dispatcher.add_handler(CommandHandler('examples', examples_command))
    updater.dispatcher.add_handler(CommandHandler('get_default_stacks', get_default_stacks))
    updater.dispatcher.add_handler(CommandHandler('get_specific_stacks', get_specific_stacks))

    updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

    updater.dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    print_before_logger(project_name=PROJECT_NAME, site=SITE)
    logger = BuildLogger(project_name=PROJECT_NAME, site=SITE).build_logger(debug=True)

    main()
