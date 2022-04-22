import re
from datetime import datetime
from telegram import Update
from typing import Union

from PythonApplications.TelegramBot.TelegramBotUserDetails import TelegramBotUserDetails
from PythonApplications.TelegramBot.FinancialStocks import financial_stocks_main
from PythonApplications.TelegramBot.StockData import StockData


def sample_user_details(user_details: TelegramBotUserDetails, input_text: str) -> Union[str, None]:
    user_massage = input_text.lower()

    if not user_details.first_name:
        user_details.first_name = user_massage.title()
        return "Thanks, what is your last name?\n"
    elif not user_details.last_name:
        user_details.last_name = user_massage.title()
        return f'Great, how can I help you {user_details.first_name} {user_details.last_name}?\n' \
               f'/start\n' \
               f'/help\n' \
               f'/examples\n'
    else:
        return None


def sample_responses(input_text: str) -> Union[str, None]:
    user_massage = input_text.lower()

    word_list_for_response = ["hello", "hi", "hey"]
    if any(user_massage.lower() == word for word in word_list_for_response):
        return 'Hey!'

    word_list_for_response = ["who are you", "who are you?"]
    if any(user_massage.lower() == word for word in word_list_for_response):
        return 'I am ABC telebot!'

    return None


def complex_responses_str(input_text: str, update: Update) -> Union[str, None]:
    user_massage = input_text.lower()

    word_list_for_response = ["what is the time", "what is the time?"]
    if any(user_massage.lower() == word for word in word_list_for_response):
        return str(datetime.now().strftime("%d/%m/%y, %H:%M:%S"))

    return None


def complex_responses_img(input_text: str, update: Update) -> Union[str, None]:
    user_massage = input_text.lower()

    word_list_for_response = ["i want stock data", "i want stock data for"]
    if any(word in user_massage.lower() for word in word_list_for_response):
        update.message.reply_text('OK, just a moment...')

        stocks = re.sub(r'i want stock data for ', '', user_massage.lower())
        stocks = re.sub(r'i want stock data', '', stocks)
        if stocks:
            stock_list = stocks.split(', ')
        else:
            stock_list = []
        return financial_stocks_main(stock_list)
        # return StockData().get_stocks(stocks=stock_list)

    return None
