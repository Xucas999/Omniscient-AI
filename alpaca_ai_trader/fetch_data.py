import pandas as pd
import alpaca_trade_api as tradeapi
from config import API_KEY, API_SECRET, BASE_URL, SYMBOL, START_DATE, END_DATE

def fetch_data():
    api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')
    bars = api.get_bars(SYMBOL, '1D', start=START_DATE, end=END_DATE).df
    bars = bars[bars['symbol'] == SYMBOL]
    bars['return'] = bars['close'].pct_change()
    bars['label'] = (bars['return'].shift(-1) > 0).astype(int)
    return bars.dropna()