import yfinance as yf
import json

def store_stock_api(period, file_name):
    """A simple function to store stock data for 5 predefined markets based on period(time).
        Parameters:
            - period -> period is the time from which stock data generated. 
                e.g. If period=5days we collect stock market from last 5 days.
            - file_name -> file path to store stock data
    """
    stock_info = []     ## storing stock data for different markets

    market_map = get_market_map()

    for name, symbol in market_map.items():
        stock_data = get_stock_data(symbol=symbol, period=period)

        if stock_data.empty:
            return 'Stock data not available, Try again later.'
        else:
            latest_close, absolute_change, percent_change = get_absolute_percent_change(stock_data=stock_data)

            stock_info.append({
                'name': name,
                'info': [latest_close, absolute_change, percent_change]
            })
    store_stock_data(stock_info, file_name)

def get_market_map():
    """Returns a dict
        Key - Stock name
        Value - Stock symbol
    """
    return {
        'NIFTY 50': '^NSEI',
        'SENSEX': '^BSESN',
        'GOLD': 'GC=F',
        'SILVER': 'SI=F',
        'USD/INR': 'USDINR=X'
    }

def get_stock_data(symbol, period):
    """Returns stock maeket data for the following symbol from specified period of time
        Returns data such as: High, Low, Volume etc, in pandas DataFrame format.
    """
    ticker = yf.Ticker(symbol)  ## creates yahoo finance object for the following stock symbol
    data = ticker.history(period)   ## Filters and gives stock market data based on period (i.e. 5d, 1y, etc.)

    return data

def get_absolute_percent_change(stock_data):
    """Returns absolute and percent change based on closing stock data."""
    latest_close = stock_data['Close'].iloc[-1]
    previous_close = stock_data['Close'].iloc[-2]

    absolute_change = latest_close - previous_close
    percent_change = (absolute_change/previous_close)* 100

    return f'{latest_close:.2f}', f'{absolute_change:.2f}', f'{percent_change:.2f}'

def store_stock_data(stock_data, file_name):
    """Storing stock data as a json formatted file."""
    with open(file_name, 'w', encoding='utf-8') as f:
        json_content = json.dumps(stock_data, indent=4)
        f.write(json_content)