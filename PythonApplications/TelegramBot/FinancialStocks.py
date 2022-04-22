import time
import yfinance as yf
import plotly.graph_objs as go


def financial_stocks_process(fig, symbols_stock_list):
    df_dict = {}
    for stock_name in symbols_stock_list:
        df_dict[stock_name] = yf.download(
            tickers=[stock_name],
            # start='2019-01-01',
            # end='2021-06-12',
            period="ytd",  # periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            # progress=False,
        )

        fig.add_trace(
            go.Scatter(
                x=df_dict[stock_name].index,
                y=df_dict[stock_name].Close,
                name=stock_name,
            )
        )
        time.sleep(0.2)


def financial_stocks_main(symbols_stock_list=None):
    if not symbols_stock_list:
        symbols_stock_list = [
            'MIMO',
            '^GSPC',
            'BTC-USD',
            'AAPL'
        ]
    fig = go.Figure()
    financial_stocks_process(
        fig=fig,
        symbols_stock_list=symbols_stock_list
    )
    # path = "output\\Financial Stocks.html"
    # fig.write_html(path)
    path = "output\\Financial Stocks.jpeg"
    fig.write_image(path)
    return path


if __name__ == '__main__':
    financial_stocks_main()
