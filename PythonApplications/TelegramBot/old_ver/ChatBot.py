import telebot
import yfinance as yf

from PrivateInfrastructure.Logger_Infrastructure.Projects_Logger import BuildLogger, print_before_logger

from PythonApplications.TelegramBot.old_ver.ChatBotDetails import ChatBotDetails

PROJECT_NAME = 'Telegram Bot'
SITE = ''

API_KEY = '2142997401:AAELi6adP_gxfgcRarNtDsM1Maoi3uLs4AA'
bot = telebot.TeleBot(API_KEY)

# ChatBotTutorial
chat_bot_details = ChatBotDetails()


@bot.message_handler(commands=['start'])
def start(message):
    global chat_bot_details
    chat_bot_details = ChatBotDetails()

    bot.reply_to(
        message,
        'Hey! Do you want to send a mail?\n\n'
        ' * You can send "/start" at any time to restart'
    )


def check_for_start_again(message):
    request = message.text.split()
    return request[0].lower() == "clear"


@bot.message_handler(func=check_for_start_again)
def lets_start_again(message):
    chat_bot_details.start['data'] = False
    start(message)


def check_for_start(message):
    request = message.text.split()
    return (
            not chat_bot_details.start['data'] and
            request[0].lower() != "yes" and
            request[0].lower() != "hey" and
            request[0].lower() != "/hello" and
            request[0].lower() != "wsb" and
            request[0].lower() != "price"
    )


@bot.message_handler(func=check_for_start)
def lets_for_start(message):
    bot.send_message(message.chat.id, 'Please send "/start" message')


@bot.message_handler(commands=['hello'])
def hello(message):
    bot.send_message(message.chat.id, "Hello!")


def hey_request(message):
    request = message.text.split()
    return request[0].lower() == "hey"


# @bot.message_handler(commands=['hello'])
@bot.message_handler(func=hey_request)
def hey(message):
    bot.reply_to(message, "Hey!")


def wsb_request(message):
    request = message.text.split()
    return request[0].lower() == "wsb"


@bot.message_handler(func=wsb_request)
def get_stocks(message):
    stocks = message.text.lower().split("wsb ")[1].split(", ")
    # stocks = ['gme', 'amc', 'nok']
    response = ""
    stock_data = []
    for stock in stocks:
        data = yf.download(tickers=stock, period='2d', interval='1d')
        data = data.reset_index()
        response += f"-----{stock}-----\n"
        stock_data.append([stock])
        columns = ['stock']
        for index, row in data.iterrows():
            stock_position = len(stock_data) - 1
            price = round(row['Close'], 2)
            format_date = row['Date'].strftime('%m/%d')
            response += f"{format_date}: {price}\n"
            stock_data[stock_position].append(price)
            columns.append(format_date)
        print()

    response = f"{columns[0] : <10}{columns[1] : ^10}{columns[2] : >10}\n"
    for row in stock_data:
        response += f"{row[0] : <10}{row[1] : ^10}{row[2] : >10}\n"
    response += "\nStock Data"
    print(response)
    bot.send_message(message.chat.id, response)


def stock_request(message):
    request = message.text.split()
    return len(request) >= 2 and request[0].lower() == "price"


@bot.message_handler(func=stock_request)
def send_price(message):
    request = message.text.split()[1]
    data = yf.download(tickers=request, period='5m', interval='1m')
    if data.size > 0:
        data = data.reset_index()
        data["format_date"] = data['Datetime'].dt.strftime('%m/%d %I:%M %p')
        data.set_index('format_date', inplace=True)
        print(data.to_string())
        bot.send_message(message.chat.id, data['Close'].to_string(header=False))
    else:
        bot.send_message(message.chat.id, "No data!?")


if __name__ == '__main__':
    print_before_logger(project_name=PROJECT_NAME, site=SITE)
    logger = BuildLogger(project_name=PROJECT_NAME, site=SITE).build_logger(debug=True)

    while True:
        try:
            logger.info('Starting Listening')
            bot.polling()
        except Exception:
            logger.exception('')
            print()
