import re
from datetime import datetime
from telegram import Update

from PythonApplications.TelegramBot.StockData import StockData


def sample_responses(input_text: str) -> str:
    user_massage = str(input_text).lower()

    word_list_for_response = ["hello", "hi", "hey"]
    if any([True if user_massage.lower() == word else False for word in word_list_for_response]):
        return 'Hey!'

    word_list_for_response = ["who are you", "who are you?"]
    if any([True if user_massage.lower() == word else False for word in word_list_for_response]):
        return 'I am ABC telebot!'

    return ''


def complex_responses(input_text: str, update: Update) -> str:
    user_massage = str(input_text).lower()

    word_list_for_response = ["what is the time", "what is the time?"]
    if any([True if user_massage.lower() == word else False for word in word_list_for_response]):
        return str(datetime.now().strftime("%d/%m/%y, %H:%M:%S"))

    word_list_for_response = ["i want stock data", "i want stock data for"]
    if any([True if word in user_massage.lower() else False for word in word_list_for_response]):
        update.message.reply_text('OK just a moment')

        stocks = re.sub(r"i want stock data for ", "", user_massage.lower())
        stocks = re.sub(r"i want stock data", "", stocks)
        stock_list = stocks. split(', ')
        return StockData().get_stocks(stocks=stock_list)

    return ''
