import logging
import yfinance as yf
import pandas as pd
from tabulate import tabulate


class StockData:
    def __init__(self):
        self.logger = logging.getLogger('Infrastructure.Logger_Infrastructure.Projects_Logger.' + self.__class__.__name__)

        self.stocks = ['MIMO', 'BTC-USD', 'MSFT', 'AAPL', 'FB', 'TWTR', 'WIX']

    def get_stocks(self, stocks=None):
        if stocks and all(v for v in stocks):
            self.stocks = stocks

        response = ""
        stock_data = []
        columns = None
        for stock in self.stocks:
            try:
                data = yf.download(tickers=stock, period='2d', interval='1d')
                data = data.reset_index()
                # data = data[['Date', 'Close']]

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
            except Exception:
                self.logger.exception(f'The stock is: {stock}')

        if stock_data and columns:
            dataframe = pd.DataFrame(stock_data, columns=[columns[0], columns[1], columns[2]])
            response = dataframe.to_markdown()

        print(response)
        return response
